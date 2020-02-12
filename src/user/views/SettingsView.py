from user.models import User
from django.views import View
from django.template import loader
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from utils.koora import get_message_or_default, generate_url_for, uploadAvatarImageFor, setInterestsFor, give_premium_to, remove_premium_from
from user.models.Card import Card


class SettingsView(View):

    def get(self, request):

        message = get_message_or_default(request, {})

        return HttpResponse(loader.get_template('user/settings.html').render({
            "page_name": "settings",
            "message": message
        }, request))

    def post(self, request):

        query = {}

        if request.POST.get("profile_update", False):
            query = self.handle_profile_update(request)

        elif request.POST.get("social_update", False):
            query = self.handle_social_update(request)

        elif request.POST.get("account_update", False):
            query = self.handle_account_update(request)

        elif request.POST.get("password_update", False):
            query = self.handle_password_update(request)

        elif request.POST.get("billing_update", False):
            query = self.handle_billing_update(request)

        return HttpResponseRedirect(generate_url_for("user:settings", query=query))

    def handle_profile_update(self, request):

        user = request.user

        user.profile.intro = request.POST.get('intro', '')
        user.profile.bio = request.POST.get('bio', '')
        user.profile.birth_date = request.POST['birth_date'] or None

        avatar_image = request.FILES.get('avatar_image', False)

        private_profile = request.POST.get('is_private', 'nope')

        user.profile.is_private = (private_profile == 'yep')

        if (avatar_image):
            uploadAvatarImageFor(user, avatar_image, user.username)

        interests = request.POST.get('interests', '').strip().split(",")

        setInterestsFor(user, interests)

        user.save()

        return {
            'type': 'success',
            'content': 'Successfully updated the profile!',
            'target': 'profile_update'
        }

    def handle_social_update(self, request):

        user = request.user

        user.profile.social.reddit_username = request.POST.get(
            'reddit_username', '')
        user.profile.social.facebook_username = request.POST.get(
            'facebook_username', '')
        user.profile.social.github_username = request.POST.get(
            'github_username', '')
        user.profile.social.discord_username = request.POST.get(
            'discord_username', '')
        user.profile.social.linkedin_username = request.POST.get(
            'linkedin_username', '')

        user.save()

        return {
            'type': 'success',
            'content': 'Successfully updated social accounts!!',
            'target': 'social_update'
        }

    def handle_account_update(self, request):

        user = request.user

        username = request.user.username
        password = request.POST.get('password', '')

        if authenticate(username=username, password=password):

            new_username = request.POST.get('username', '')

            if new_username != username and User.objects.filter(username=new_username).exists():

                return {
                    "type": "danger",
                    "content": "Username : '{}' has already been taken".format(new_username),
                    'target': 'account_update'
                }

            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')

            user.username = new_username

            user.save()

            return {
                'type': 'success',
                'content': 'Your account has been updated successfully!!',
                'target': 'account_update'
            }

        else:
            return {
                'type': 'danger',
                'content': 'Incorrect password entered, Please try again!',
                'target': 'account_update'
            }

    def handle_password_update(self, request):

        user = request.user

        username = user.username
        old_password = request.POST.get('old_password', '')

        new_password = request.POST.get('new_password', '')
        new_password_repeat = request.POST.get('new_password_repeat', '')

        if new_password != new_password_repeat:

            return {
                'type': 'danger',
                'content': "Passwords don't match!",
                'target': 'password_update'
            }

        elif not authenticate(username=username, password=old_password):
            return {
                'type': 'danger',
                'content': 'Incorrect password entered, Please try again!',
                'target': 'password_update'
            }

        user.set_password(new_password)

        user.save()

        return {
            'type': 'success',
            'content': 'Password changed successfully!',
            'target': 'password_update'
        }

    def handle_billing_update(self, request):
        user = request.user

        username = request.user.username
        password = request.POST.get('password', '')

        if authenticate(username=username, password=password):

            card_holder = request.POST.get('card_holder', False)
            card_number = request.POST.get('card_number', False)
            exp_date = request.POST.get('exp_date', False)
            cvc = request.POST.get('cvc', False)

            first_premium = False

            if card_holder and card_number and exp_date and cvc:

                if not user.profile.is_premium:
                    card = Card.objects.create(
                        card_holder=card_holder, card_number=card_number, exp_date=exp_date, cvc=cvc)
                    user.profile.card = card
                    user.profile.is_premium = True
                    give_premium_to(user)
                    first_premium = True

                else:
                    user.profile.card.card_holder = card_holder
                    user.profile.card.card_number = card_number
                    user.profile.card.exp_date = exp_date
                    user.profile.card.cvc = cvc

            elif user.profile.card:
                user.profile.card = None
                remove_premium_from(user)
                user.profile.is_premium = False

            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')

            user.profile.location.country = request.POST.get('country', '')
            user.profile.location.address = request.POST.get('address', '')
            user.profile.location.province = request.POST.get('province', '')
            user.profile.location.city = request.POST.get('city', '')
            user.profile.location.zip_code = request.POST.get('zip_code', '')

            user.save()

            return {
                'type': 'success',
                'content': 'Your Billing Information has been updated successfully{}!'.format(
                    '  You are now a Premium User' if first_premium else ''
                ),
                'target': 'billing_update'
            }

        else:
            return {
                'type': 'danger',
                'content': 'Incorrect password entered, Please try again!',
                'target': 'billing_update'
            }

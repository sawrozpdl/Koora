from django.contrib import admin

from .models import Profile
from .models import Location
from .models import Card
from .models import Social

admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Card)
admin.site.register(Social)


def login_required(*margs, **mkwargs):
    def real_decorator(func):
        def wrapper(*args, **kwargs):
            if req["user"]["is_authenticated"]:
                return func(*args, **kwargs)
            else:
                print('you are not authenticated! go talk to -> ', margs[0])
        return wrapper
    return real_decorator
    

    
@login_required('admin')
def show_content(request):   # this is equivalent to : login_required('admin')(show_content)(request)
    print('You are authenticated! Here\'s your content);    
    
    
req = {
    "user" : {
        "is_authenticated" : False
    }
}
    

show_content(req) # output => you are not authenticated! go talk to -> admin
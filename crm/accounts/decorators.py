from django.http import HttpResponse
from django.shortcuts import redirect

# a decorator is a function which takes another function in as a parameter and allow us to add some functionality to our main function in our view


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # if user is authenticated, redirect to home, else, run our function in views (loginPage)
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


# the decorator is placed on top of a view,
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                # the group is the name of the group related to that user
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator


# Don't do this in a real project. we check the group type
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('user-page')

        if group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper_func

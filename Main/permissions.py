from functools import wraps
from django.http import HttpResponseRedirect
from django.shortcuts import render

def garage_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'garage':
            return function(request, *args, **kwargs)
        else:
            return render(request, 'access_denied.html', status=403)
    return wrap


def superuser_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            return render(request, 'access_denied.html', status=403)
    return wrap

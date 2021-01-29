from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test


def guest_middleware(call):
    def check(request):

        call(request)
        if request.user:
            if request.user.id and isinstance(request.user.id, int):
                return redirect('/')
        return True
    return check

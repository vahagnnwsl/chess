from django.shortcuts import render, redirect
from account.forms import RegisterForm, LoginForm, ChangePasswordForm
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages


@require_http_methods(["GET"])
def register_get(request):
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'account/pages/register.html', {'form': RegisterForm, 'request': request})


@require_http_methods(["POST"])
def register_post(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('account')
    else:
        return render(request, 'account/pages/register.html', {'form': form})


@require_http_methods(["GET"])
def login_get(request):
    if request.user.is_authenticated:
        return redirect('/')

    return render(request, 'account/pages/login.html', {'form': LoginForm, 'request': request})


@require_http_methods(["POST"])
def login_post(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

        if user is not None:
            login(request, user)
            return redirect('account')

        return render(request, 'account/pages/login.html', {'form': LoginForm})

    else:

        return render(request, 'account/pages/login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('home')


@require_http_methods(["GET"])
@login_required
def account(request):
    return render(request, 'account/pages/account.html')


@require_http_methods(["POST", "GET"])
@login_required
def password(request):
    
    if request.method == 'GET':

        return render(request, 'account/pages/account.html',
                      { 'form': ChangePasswordForm(request.user)})
    else:

        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            return render(request, 'account/pages/account.html', { 'form': form})

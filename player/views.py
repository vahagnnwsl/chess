from django.shortcuts import render, redirect
from django.views import View
from player.forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


class RegisterView(View):
    template_name = 'player/pages/register.html'
    form_class = RegisterForm

    def get(self, request):

        if request.user.is_authenticated:
            return redirect('/')

        return render(request, self.template_name, {'form': self.form_class(), 'request': request})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account')
        else:
            return render(request, self.template_name, {'form': form, 'request': request})


class LoginView(View):
    template_name = 'player/pages/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect('/')

        return render(request, self.template_name, {'form': self.form_class(), 'request': request})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user is not None:
                login(request, user)
                return redirect('account')

            return render(request, self.template_name, {'form': self.form_class(), 'request': request})

        else:

            return render(request, self.template_name, {'form': form, 'request': request})


@require_http_methods(["GET"])
@login_required
def account(request):
    return render(request, 'player/pages/account.html', {'request': request})


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    return redirect('home')





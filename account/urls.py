from django.urls import path, re_path
from account.views import *

urlpatterns = [
    path('', account, name='account'),
    path('/password', password, name='account_password'),
    path('/statistics', account, name='account_statistics'),
    path('/history', history, name='account_history'),
    re_path(r'^/login/$', login_get, name='login'),
    path('/login_post', login_post, name='login_post'),
    path('/register', register_get, name='register'),
    path('/register_post', register_post, name='register_post'),
    path('/logout', logout_view, name='logout')
]

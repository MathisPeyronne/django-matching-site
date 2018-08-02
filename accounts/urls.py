"""matchmaking_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),


    # login
    path('login/', views.user_login, name='login'),
    
    #logout(uses django views)
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out_2.html'), name='logout'), #il confond avec le logged out du admin site si on change pas le nom

    # change password urls(uses django views)
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form_2.html'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done_2.html'), name='password_change_done'),

    # restore password urls(uses django views)
    # email_template_name='email.html' because default is the one of the admin site.
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form_2.html',email_template_name='registration/password_reset_email_2.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done_2.html'), name='password_reset_done'),
    re_path(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #erace friend
    re_path('delete_friend/(?P<username>[-\w]+)/$', views.delete_friend, name='delete_friend'),

    #close account
    path('delete_account/', views.delete_account, name='delete_account')


]
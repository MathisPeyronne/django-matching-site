from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile
from Dashboard.models import Message


class FriendsEditForm(forms.Form):
    friend = forms.CharField(max_length=30,  label='add a friend:', help_text='once at the time, max 10')

class MessageForm(forms.Form):
    message = forms.CharField(max_length="250", label="")

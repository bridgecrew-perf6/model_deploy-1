from django import forms
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm

from .models import Profile

# this class inherits from UserCreationForm


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:

		model = User
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = []
from django import forms
from study_app.models import User

class RegistrationForm(forms.Form):
	username = forms.CharField(
		label='Username', 
		max_length = 40, 
		required=True
	)
	email = forms.EmailField(
		label='Email',
		max_length = 100,
		required=True
	)
	password = forms.CharField(
		label='Password',
		widget=forms.PasswordInput(),
		max_length = 100,
		required=True
	)
	confirmPassword = forms.CharField(
		label='Confirm Password',
		widget=forms.PasswordInput(),
		max_length = 100,
		required=True
	)
	avatar = forms.ImageField(
		label='Avatar',
		required=False
	)
	tosCheck = forms.NullBooleanField(
		label='I agree to Terms of Service',
        widget=forms.CheckboxInput()
	)

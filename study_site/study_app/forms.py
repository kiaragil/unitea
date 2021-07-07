from django import forms
from study_app.models import User

class RegistrationForm(forms.ModelForm):
	class Meta:
		model = User
		fields = "__all__"
from django import forms
from study_app.models import *

SUBJECT_CHOICES = (
    ('', ''),
    ('math', 'Math'),
    ('science', 'Science'),
    ('languages', 'Languages'),
    ('economics', 'Economics'),
    ('history', 'History'),
    ('business', 'Business'),
)


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=40,
        required=True
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True
    )
    confirmPassword = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True
    )
    tosCheck = forms.NullBooleanField(
        label='I agree to Terms of Service',
        widget=forms.CheckboxInput()
    )


class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        # add attribute for id:avatar-input
    )
    # avatar.widget.attrs({'class':'materialize-textarea'})   
    profile = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )
    profile.widget.attrs.update({'class':'materialize-textarea'})

    class Meta:
        model = User
        fields = ['username', 'avatar', 'profile']


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=True
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True
    )


class ContactForm(forms.Form):
    fullname = forms.CharField(
        label='Full Name',
        max_length=45,
        required=True
    )
    telephone = forms.CharField(
        label='Telephone',
        max_length=15,
        required=True
    )
    email = forms.EmailField(
        label='Email',
        max_length=45,
        required=True
    )
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(),
        max_length=200,
        required=True
    )


class StudyGroupForm(forms.ModelForm):
    groupName = forms.CharField(
        label='Study Group Name', 
        max_length = 100, 
        required=True
    )
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(),
        max_length=5000,
        required=True
    )
    description.widget.attrs.update({'class':'materialize-textarea'})
    description.widget.attrs.update({'id':'editSGP-text'})   
    subject = forms.CharField(
        label='Subject', 
        widget=forms.Select(choices=SUBJECT_CHOICES),
        required=False
    )
    subject.widget.attrs.update({'class':'editSGP-subject'})

    class Meta:
        model = StudyGroup
        fields = ['groupName', 'description', 'subject']


class MainPostForm(forms.ModelForm):
    postTitle = forms.CharField(
        label='Title'
    )
    post = forms.CharField(
        label='Description',
        widget=forms.Textarea(),
    )
    post.widget.attrs.update({'class':'materialize-textarea'})
    post.widget.attrs.update({'id':'editMP-text'})    

    class Meta:
        model = MainPost
        fields = ['postTitle', 'post']


class MainCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea(),
    )
    comment.widget.attrs.update({'class':'materialize-textarea'})

    class Meta:
        model = MainComment
        fields = ['comment']


class StudyGroupPostForm(forms.ModelForm):
    postTitle = forms.CharField(
        label='Title'
    )
    post = forms.CharField(
        label='Description',
        widget=forms.Textarea(),
    )

    post.widget.attrs.update({'class':'materialize-textarea'})
    post.widget.attrs.update({'id':'editSGP-text'})   
    class Meta:
        model = StudyGroupPost
        fields = ['postTitle', 'post']


class StudyGroupCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(),
    )

    class Meta:
        model = StudyGroupComment
        fields = ['comment']


class MessageForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(),
    )

    class Meta:
        model = Message
        fields = ['message']


class UserPasswordForm(forms.Form):
    currentPassword = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True
    )
    newPassword = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True
    )
    confirmPassword = forms.CharField(
        label='Confirm New Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True
    )
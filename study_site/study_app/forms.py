"""
Class: CSC648-848 SW Engineering SU21
Team: Team 4
Name: Kiara Gil, Ostyn Sy, Joshua Stone, Cong Le, Miho Shimizu, Vernon Xie, Melinda Yee
GitHub Name: KiaraGil, OstynSy, JoshLikesToCode, CleGuren, simicity, vxie123, melinda15

File Name: forms.py

Description: This file includes all forms on the website
ex. Login, Register, contact, studygroup, etc
"""

from django import forms
from study_app.models import *

INSTITUTE_CHOICES = (
    ('', 'Select Institute'),
    ('SF State University', 'SF State University'),
)

SUBJECT_CHOICES = (
    ('', 'Select subject'),
    ('math', 'Math'),
    ('science', 'Science'),
    ('languages', 'Languages'),
    ('economics', 'Economics'),
    ('history', 'History'),
    ('business', 'Business'),
)


# Form for registration
class RegistrationForm(forms.Form):

    username = forms.CharField(
        label='Username',
        max_length=40,
        required=True,
    )
    email = forms.EmailField(
        label='Email',
        max_length=100,
        required=True,
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        max_length=100,
        required=True,
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
    institute = forms.CharField(
        label = 'What institute are you teaching at?',
        widget=forms.Select(choices=INSTITUTE_CHOICES),
        required=True,
    )
    field = forms.CharField(
        label = 'What field are you teaching?',
        max_length=100,
        required=True,
    )


# Edit User Profile Form
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


# Login Form
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


# Contact Form
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


# Study Group Form
class StudyGroupForm(forms.ModelForm):
    groupName = forms.CharField(
        label='Study Group Name',
        max_length=100,
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
        required=True
    )
    subject.widget.attrs.update({'class':'editSGP-subject'})

    class Meta:
        model = StudyGroup
        fields = ['groupName', 'description', 'subject']


# Main Forum Post Form
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


# Main Forum Commenting Form
class MainCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='Comment',
        widget=forms.Textarea(),
    )
    comment.widget.attrs.update({'class':'materialize-textarea'})


    class Meta:
        model = MainComment
        fields = ['comment']


# Create Study Group Post Form
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


# Study Group Comment Form
class StudyGroupCommentForm(forms.ModelForm):
    comment = forms.CharField(
        widget=forms.Textarea(),
    )
    comment.widget.attrs.update({'class':'materialize-textarea'})

    class Meta:
        model = StudyGroupComment
        fields = ['comment']


# Change User Password Form
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
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

# Create your models here.

ROLE_CHOICES = (
	('general', 'general'),
	('educator', 'educator'),
	('admin', 'admin')
)


class User(AbstractBaseUser):
	userId = models.AutoField(primary_key=True, unique=True)
	username = models.CharField(max_length=40, unique=True)
	email = models.EmailField(max_length=100)
	password = models.CharField(max_length=100)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='general')
	avatar = models.ImageField(upload_to='images/')
	last_login = None

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'role']

	objects = UserManager()

	def __str__(self):
		return self.username

	class Meta:
		db_table = "users";


class MainPost(models.Model):
	postId = models.AutoField(primary_key=True, unique=True)
	postTitle = models.CharField(max_length=100)
	post = models.CharField(max_length=5000)
	postDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		db_table = "mainposts";


class MainComment(models.Model):
	commentId = models.AutoField(primary_key=True, unique=True)
	comment = models.CharField(max_length=5000)
	commentDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	postId = models.ForeignKey(MainPost, on_delete=models.CASCADE)

	class Meta:
		db_table = "maincomments";


class StudyGroup(models.Model):
	studyGroupId = models.AutoField(primary_key=True, unique=True)
	groupName = models.CharField(max_length=100)
	description = models.CharField(max_length=5000)
	ownerId = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		db_table = "studygroups";


class StudyGroupPost(models.Model):
	postId = models.AutoField(primary_key=True, unique=True)
	postTitle = models.CharField(max_length=100)
	post = models.CharField(max_length=5000)
	postDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

	class Meta:
		db_table = "studygroupposts";


class StudyGroupComment(models.Model):
	commentId = models.AutoField(primary_key=True, unique=True)
	comment = models.CharField(max_length=5000)
	commentDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	postId = models.ForeignKey(StudyGroupPost, on_delete=models.CASCADE)

	class Meta:
		db_table = "studygroupcomments";


class Member(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

	class Meta:
		db_table = "members";


class Contact(models.Model):
	fullname = models.CharField(max_length=45)
	telephone = models.CharField(max_length=15)
	email = models.EmailField(max_length=45)
	message = models.CharField(max_length=200)

	class Meta:
		db_table = "contactus";
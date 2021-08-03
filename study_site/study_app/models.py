"""
Class: CSC648-848 SW Engineering SU21
Team: Team 4
Name: Kiara Gil, Ostyn Sy, Joshua Stone, Cong Le, Miho Shimizu, Vernon Xie, Melinda Yee
GitHub Name: KiaraGil, OstynSy, JoshLikesToCode, CleGuren, simicity, vxie123, melinda15
GitHub URL: https://github.com/sfsu-joseo/csc648-848-sw-engineering-SU21-T04

File Name: models.py

Description: Creates models of objects that connect variables to our database.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager

# Create your models here.

# User Roles
ROLE_CHOICES = (
	('general', 'general'),
	('educator', 'educator'),
	('admin', 'admin')
)

# Roles for Group Type
GROUP_TYPE_CHOICES = (
	('general', 'general'),
	('educator', 'educator'),
)

# Group Capacities
STUDY_GROUP_CAPACITY = 20
EDUCATOR_STUDY_GROUP_CAPACITY = 50


# User Model
class User(AbstractBaseUser):
	userId = models.AutoField(primary_key=True, unique=True)
	username = models.CharField(max_length=40, unique=True)
	email = models.EmailField(max_length=100, unique=True)
	password = models.CharField(max_length=100)
	role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='general')
	avatar = models.ImageField(upload_to='images/')
	profile = models.CharField(max_length=1000, blank=True, null=True)
	last_login = None

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'role']

	objects = UserManager()

	def __str__(self):
		return self.username

	class Meta:
		db_table = "users";


# Main Post Model
class MainPost(models.Model):
	postId = models.AutoField(primary_key=True, unique=True)
	postTitle = models.CharField(max_length=100)
	post = models.CharField(max_length=5000)
	postDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		db_table = "mainposts";


# Main Comment Model
class MainComment(models.Model):
	commentId = models.AutoField(primary_key=True, unique=True)
	comment = models.CharField(max_length=5000)
	commentDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	postId = models.ForeignKey(MainPost, on_delete=models.CASCADE)

	class Meta:
		db_table = "maincomments";


# Study Group Model
class StudyGroup(models.Model):
	studyGroupId = models.AutoField(primary_key=True, unique=True)
	groupName = models.CharField(max_length=100)
	description = models.CharField(max_length=5000)
	groupType = models.CharField(max_length=10, choices=GROUP_TYPE_CHOICES, default='general')
	memberCount = models.IntegerField(default=0)
	subject = models.CharField(max_length=100, blank=True, null=True)
	ownerId = models.ForeignKey(User, on_delete=models.CASCADE)

	def isFull(self):
		if self.ownerId.role == "educator":
			return True if self.memberCount >= EDUCATOR_STUDY_GROUP_CAPACITY else False
		else:
			return True if self.memberCount >= STUDY_GROUP_CAPACITY else False

	class Meta:
		db_table = "studygroups";


# Study Group Post Model
class StudyGroupPost(models.Model):
	postId = models.AutoField(primary_key=True, unique=True)
	postTitle = models.CharField(max_length=100)
	post = models.CharField(max_length=5000)
	postDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

	class Meta:
		db_table = "studygroupposts";


# Study Group Comment Model
class StudyGroupComment(models.Model):
	commentId = models.AutoField(primary_key=True, unique=True)
	comment = models.CharField(max_length=5000)
	commentDateTime = models.DateTimeField(auto_now=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	postId = models.ForeignKey(StudyGroupPost, on_delete=models.CASCADE)

	class Meta:
		db_table = "studygroupcomments";


# Study Group Member Model
class StudyGroupMember(models.Model):
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	studyGroupId = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)

	class Meta:
		db_table = "studygroupmembers";


# Contact Model
class Contact(models.Model):
	fullname = models.CharField(max_length=45)
	telephone = models.CharField(max_length=15)
	email = models.EmailField(max_length=45)
	message = models.CharField(max_length=200)

	class Meta:
		db_table = "contactus";
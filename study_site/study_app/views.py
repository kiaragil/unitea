from django.shortcuts import render, redirect
from django.template import loader
from study_app.forms import *
from study_app.models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

#show landing page to general users and homepage to logged in users
def index(request):
    #not logged in users don't access the landing page
    if not request.user.is_authenticated:
        return redirect('/landing')

    return render(request, 'index.html')

#show homepage
def home(request):
    return render(request, 'index.html')

#show the contact us page
def contactusPage(request):
    context = {}
    context['form'] = ContactForm()
    return render(request, "contactus.html", context)

#submits the contact us form
def submitContactus(request):
    context = {}
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = Contact()
            contact.fullname = form.cleaned_data['fullname']
            contact.telephone = form.cleaned_data['telephone']
            contact.email = form.cleaned_data['email']
            contact.message = form.cleaned_data['message']
            contact.save()
            return redirect('/contactus')
        else:
            print("Form not valid")
            context['form'] = form
    else:
        context['form'] = ContactForm()
    return render(request, 'contactus.html', context)


def construction(request):
    return render(request, 'construction.html')


def about(request):
    return render(request, 'about.html')

#show landing page
def landing(request):
    #logged in users don't access the landing page
    if request.user.is_authenticated:
        print("user is already logged in")
        return redirect('/')

    return render(request, 'landing.html')


def aboutUs(request, member):
    template = loader.get_template('about/T4TM-{name}.html'.format(name=member))
    context = {}
    return HttpResponse(template.render(context, request))


# ----------------------------
#  User
# ----------------------------

#show the user registration page
def register(request):
    #logged in users must not access 
    if request.user.is_authenticated:
        print("user is already logged in")
        return redirect('/')

    context = {}
    context['form'] = RegistrationForm()
    return render(request, "register.html", context)

#create a user account
def createUser(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['tosCheck']:
            user = User()
            user.username = form.cleaned_data['username']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user.confirmPassword = form.cleaned_data['confirmPassword']

            #password and confirm password must match
            if user.password == user.confirmPassword:
                try:
                    #hash password
                    user.password = make_password(user.password)
                    #register a user
                    messages.success(request, "New account created!")
                    user.save()
                    return redirect('/login')
                except:
                    pass
            else:
                messages.error(request, "Confirm password doesn't match")
                context['form'] = form
        else:
            messages.error(request, "Invalid form data")
            context['form'] = form
    else:
        messages.error(request, "Something is wrong")
        context['form'] = RegistrationForm()

    #user creation failed
    return render(request, 'register.html', context)

#show the edit user profile page
def editUserProfile(request):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    user = User.objects.get(userId=request.user.userId)
    context = {}
    context['form'] = UserProfileForm(instance = user)
    return render(request, 'edituserprofile.html', context)

#update user profile
def updateUserProfile(request):
    context = {}
    user = User.objects.get(userId=request.user.userId)
    form = UserProfileForm(request.POST, instance = user)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'edituserprofile.html', context)

#show the login page
def loginPage(request):
    #logged in users must not access 
    if request.user.is_authenticated:
        print("user is already logged in")
        return redirect('/')

    context = {}
    context['form'] = LoginForm()
    return render(request, "login.html", context)

#let a user login
def loginUser(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                messages.success(request, "You are successfully logged in!")
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Authentication failed")
                context['form'] = form
        else:
            messages.error(request, "Invalid form data")
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'login.html', context)

#let a user logout
def logoutUser(request):
    messages.success(request, "You are logged out!")
    logout(request)
    return redirect('/')

#delete a user account
def deleteUser(request):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/login')

    #delete the currently logged in user
    user = User.objects.get(userId=request.user.userId)
    user.delete()
    return redirect('/')

#show a specified user's profile
def showUserProfile(request, userId):
    user = User.objects.get(userId=userId)
    return render(request, 'profile.html', {'user': user})


# ----------------------------
#  Main Forum Post
# ----------------------------

#show main forum
def showMainForum(request):
    mainposts = MainPost.objects.all()
    return render(request, 'mainforum.html', {'mainposts': mainposts})

#show a main post
def showMainPost(request, postId):
    mainpost = MainPost.objects.get(postId=postId)
    comments = MainComment.objects.all()
    form = MainCommentForm()
    return render(request, 'mainPostPage.html', {'mainpost': mainpost, 'comments': comments, 'form':form})

#show the main post creation page
def createMainPost(request):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = MainPostForm()
    return render(request, "createMainPost.html", context)

#create a main post
def execCreateMainPost(request):
    context = {}
    if request.method == "POST":
        form = MainPostForm(request.POST)
        if form.is_valid():
            mainPost = MainPost()
            mainPost.postTitle = form.cleaned_data['postTitle']
            mainPost.post = form.cleaned_data['post']
            #owner is the currently logged in user
            mainPost.userId = User.objects.get(userId=request.user.userId)
            try:
                messages.success(request, "New post created")
                mainPost.save()
                return redirect('/mainforum')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    context['form'] = MainPostForm()
    return render(request, 'createMainPost.html', context)

#show the edit post page
def editMainPost(request, postId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    mainPost = MainPost.objects.get(postId=postId)
    context = {}
    context['form'] = MainPostForm(instance = mainPost)
    return render(request, 'editMainPost.html', context)

#update a main post
def updateMainPost(request, postId):
    context = {}
    mainPost = MainPost.objects.get(postId=postId)
    form = MainPostForm(request.POST, instance=mainPost)
    if form.is_valid():
        form.save()
        return redirect(f'/{postId}/mainpost')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'editMainPost.html', context)

#delete a main post
def deleteMainPost(request, postId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/login')

    mainPost = MainPost.objects.get(postId=postId)
    mainPost.delete()
    return redirect('/mainforum')


# ----------------------------
#  Main Forum Post Comment
# ----------------------------

#show the main comment creation page (currently not in use)
def createMainComment(request, postId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = MainCommentForm()
    return render(request, "createMainComment.html", context)

#create a comment for a main post
def execCreateMainComment(request, postId):
    context = {}
    if request.method == "POST":
        form = MainCommentForm(request.POST)
        if form.is_valid():
            mainComment = MainComment()
            mainComment.comment = form.cleaned_data['comment']
            #owner is the currently logged in user
            mainComment.userId = User.objects.get(userId=request.user.userId)
            mainComment.postId = MainPost.objects.get(postId=postId)
            try:
                messages.success(request, "New post created")
                mainComment.save()
                return redirect(f'/{postId}/mainpost')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    context['form'] = MainCommentForm()
    return render(request, 'createMainComment.html', context)

#show the edit main comment page
def editMainComment(request, postId, commentId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    mainComment = MainComment.objects.get(commentId=commentId)
    context = {}
    context['form'] = MainCommentForm(instance = mainComment)
    return render(request, 'editMainComment.html', context)

#update a main comment
def updateMainComment(request, postId, commentId):
    context = {}
    mainComment = MainComment.objects.get(commentId=commentId)
    form = MainCommentForm(request.POST, instance=mainComment)
    if form.is_valid():
        form.save()
        return redirect(f'/{postId}/mainpost')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'editMainComment.html', context)

#delete a main comment
def deleteMainComment(request, postId, commentId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/login')

    mainComment = MainComment.objects.get(commentId=commentId)
    mainComment.delete()
    return redirect(f'/{postId}/mainpost')


# ----------------------------
#  Study Group
# ----------------------------

#show study group listing
def showStudyGroupListing(request, subject):
    studyGroups = StudyGroup.objects.filter(subject__contains=subject)
    return render(request, 'studyGroupListing.html', {'studygroups': studyGroups})

#show a study group page
def showStudyGroup(request, studyGroupId):
    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    studygroupposts = StudyGroupPost.objects.filter(studyGroupId=studyGroupId)
    return render(request, 'studyGroupPage.html', {'studygroup': studygroup, 'studygroupposts': studygroupposts})

#show the study group creation page
def createStudyGroup(request):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = StudyGroupForm()
    return render(request, "createStudyGroup.html", context)

#create a study group
def execCreateStudyGroup(request):
    context = {}
    if request.method == "POST":
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            studyGroup = StudyGroup()
            studyGroup.groupName = form.cleaned_data['groupName']
            studyGroup.description = form.cleaned_data['description']
            studyGroup.subject = form.cleaned_data['subject']
            #owner is the currently logged in user
            studyGroup.ownerId = User.objects.get(userId=request.user.userId)
            try:
                messages.success(request, "New study group created")
                studyGroup.save()
                return redirect(f'/{studyGroup.studyGroupId}/studygroup')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    context['form'] = StudyGroupForm()
    return render(request, 'createStudyGroup.html', context)

#show the edit study group page
def editStudyGroup(request, studyGroupId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    context = {}
    context['form'] = StudyGroupForm(instance = studygroup)
    return render(request, 'editStudyGroup.html', context)

#update a study group
def updateStudyGroup(request, studyGroupId):
    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    form = StudyGroupForm(request.POST, instance=studygroup)
    if form.is_valid():
        form.save()
        return redirect(f'/{studyGroupId}/studygroup')
    else:
        messages.error(request, "Invalid form data")
    context = {}
    context['form'] = form
    return render(request, 'editStudyGroup.html', context)

#delete a study group
def deleteStudyGroup(request, studyGroupId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/login')

    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    studygroup.delete()
    return redirect('/home')

#check if the logged in user is a member of the study group
def isMember(request, studyGroupId):
    studyGroupMember = StudyGroupMember.objects.filter(userId=request.user.userId, studyGroupId=studyGroupId)
    return True if studyGroupMember else False

#let the logged in user join a study group
def joinStudyGroup(request, studyGroupId):
    studyGroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    if not studyGroup.isFull() and not isMember(request, studyGroupId):
        studyGroupMember = StudyGroupMember()
        studyGroupMember.userId = User.objects.get(userId=request.user.userId)
        studyGroupMember.studyGroupId = studyGroup
        studyGroupMember.save()

        studyGroup.memberCount += 1
        studyGroup.save()
    return redirect(f'/{studyGroupId}/studygroup')

#let the logged in user leave a study group
def leaveStudyGroup(request, studyGroupId):
    studyGroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    if studyGroup.memberCount > 0:
        studyGroup.memberCount -= 1
    
    studyGroupMember = StudyGroupMember.objects.filter(userId=request.user.userId, studyGroupId=studyGroupId)
    studyGroupMember.delete()
    return redirect(f'/{studyGroupId}/studygroup')

#search study groups
def searchStudyGroups(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if not searched:
            messages.info(request, "Please enter a search word")
            return redirect('/home')
        studyGroups = StudyGroup.objects.filter(groupName__contains=searched)
        return render(request, 'searchResults.html', {'searched': searched, 'studygroups': studyGroups})
    else:
        return redirect('/home')


# ----------------------------
#  Study Group Forum Post
# ----------------------------

#show a study group post
def showStudyGroupPost(request, studyGroupId, postId):
    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    studygrouppost = StudyGroupPost.objects.get(postId=postId)
    comments = StudyGroupComment.objects.all()
    form = StudyGroupCommentForm()
    return render(request, 'studyGroupPostPage.html', {'studygroup': studygroup, 'studygrouppost': studygrouppost, 'comments': comments, 'form': form})

#show the study group post creation page
def createStudyGroupPost(request, studyGroupId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = StudyGroupPostForm()
    return render(request, "createStudyGroupPost.html", context)

#create a study group forum post
def execCreateStudyGroupPost(request, studyGroupId):
    context = {}
    if request.method == "POST":
        form = StudyGroupPostForm(request.POST)
        if form.is_valid():
            studyGroupPost = StudyGroupPost()
            studyGroupPost.postTitle = form.cleaned_data['postTitle']
            studyGroupPost.post = form.cleaned_data['post']
            #owner is the currently logged in user
            studyGroupPost.userId = User.objects.get(userId=request.user.userId)
            studyGroupPost.studyGroupId = StudyGroup.objects.get(studyGroupId=studyGroupId)
            try:
                messages.success(request, "New post created")
                studyGroupPost.save()
                return redirect(f'/{studyGroupId}/studygroup')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    context['form'] = StudyGroupPostForm()
    return render(request, 'createStudyGroupPost.html', context)

#show the edit study group forum post page
def editStudyGroupPost(request, studyGroupId, postId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    studyGroupPost = StudyGroupPost.objects.get(postId=postId)
    context = {}
    context['form'] = StudyGroupPostForm(instance = studyGroupPost)
    return render(request, 'editStudyGroupPost.html', context)

#update a study group forum post
def updateStudyGroupPost(request, studyGroupId, postId):
    context = {}
    studyGroupPost = StudyGroupPost.objects.get(postId=postId)
    form = StudyGroupPostForm(request.POST, instance=studyGroupPost)
    if form.is_valid():
        form.save()
        return redirect(f'/{studyGroupId}/{postId}/studygrouppost')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'editStudyGroupPost.html', context)

#delete a study group forum post
def deleteStudyGroupPost(request, studyGroupId, postId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/login')

    studyGroupPost = StudyGroupPost.objects.get(postId=postId)
    studyGroupPost.delete()
    return redirect(f'/{studyGroupId}/studygroup')


# ----------------------------
#  StudyGroup Forum Post Comment
# ----------------------------

#show the study group comment page (currently not in use)
def createStudyGroupComment(request, studyGroupId, postId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = StudyGroupCommentForm()
    return render(request, "createStudyGroupComment.html", context)

# create a comment for a study group forum post
def execCreateStudyGroupComment(request, studyGroupId, postId):
    context = {}
    if request.method == "POST":
        form = StudyGroupCommentForm(request.POST)
        if form.is_valid():
            studyGroupComment = StudyGroupComment()
            studyGroupComment.comment = form.cleaned_data['comment']
            #owner is the currently logged in user
            studyGroupComment.userId = User.objects.get(userId=request.user.userId)
            studyGroupComment.postId = StudyGroupPost.objects.get(postId=postId)
            try:
                messages.success(request, "New post created")
                studyGroupComment.save()
                return redirect(f'/{studyGroupId}/{postId}/studygrouppost')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    context['form'] = StudyGroupCommentForm()
    return render(request, 'createStudyGroupComment.html', context)

#show the edit study group comment page
def editStudyGroupComment(request, studyGroupId, postId, commentId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    studyGroupComment = StudyGroupComment.objects.get(commentId=commentId)
    context = {}
    context['form'] = StudyGroupCommentForm(instance = studyGroupComment)
    return render(request, 'editStudyGroupComment.html', context)

#update a study group comment
def updateStudyGroupComment(request, studyGroupId, postId, commentId):
    context = {}
    studyGroupComment = StudyGroupComment.objects.get(commentId=commentId)
    form = StudyGroupCommentForm(request.POST, instance=studyGroupComment)
    if form.is_valid():
        form.save()
        return redirect(f'/{studyGroupId}/{postId}/studygrouppost')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'editStudyGroupComment.html', context)

#delete a study group comment
def deleteStudyGroupComment(request, studyGroupId, postId, commentId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/login')

    studyGroupComment = StudyGroupComment.objects.get(commentId=commentId)
    studyGroupComment.delete()
    return redirect(f'/{studyGroupId}/{postId}/studygrouppost')


# ----------------------------
#  Front End Testing 
# ----------------------------

def testEditStudyGroup(request):
    return render(request, 'testEditStudyGroup.html')

def testCreateStudyPost(request):
    return render(request, 'testCreateStudyPost.html')

def testCreateMainPost(request):
    return render(request, 'testCreateMainPost.html')

def testEditMainPost(request):
    return render(request, 'testEditMainPost.html')

def testEditStudyGroupPost(request):
    return render(request, 'testEditStudyGroupPost.html')

def report(request):
    return render(request, 'report.html')

def testUserProfile(request):
    return render(request, 'testUserProfile.html')

def testEditUserProfile(request):
    return render(request, 'testEditUserProfile.html')
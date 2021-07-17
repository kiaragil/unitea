from django.shortcuts import render, redirect
from django.template import loader
from study_app.forms import *
from study_app.models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})


def contactusPage(request):
    context = {}
    context['form'] = ContactForm()
    return render(request, "contactus.html", context)


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


def landing(request):
    return render(request, 'landing.html')


def aboutUs(request, member):
    template = loader.get_template('about/T4TM-{name}.html'.format(name=member))
    context = {}
    return HttpResponse(template.render(context, request))


def showForum(request):
    mainposts = MainPost.objects.all()
    studygroups = StudyGroup.objects.all()
    return render(request, 'forums.html', {'mainposts': mainposts, 'studygroups': studygroups})


def showMainPost(request, postId):
    mainpost = MainPost.objects.get(postId=postId)
    comments = MainComment.objects.all()
    form = MainCommentForm()
    return render(request, 'mainPostPage.html', {'mainpost': mainpost, 'comments': comments, 'form':form})


def showStudyGroupPost(request, studyGroupId):
    studygroup = StudyGroupPost.objects.all(studyGroupId=studyGroupId)
    comments = StudyGroupComment.objects.all()
    form = StudyGroupCommentForm()
    return render(request, 'studyGroupPage.html', {'studygroup': studygroup, 'comments': comments, 'form': form})


# ----------------------------
#  User
# ----------------------------

def register(request):
    #logged in users must not access 
    if request.user.is_authenticated:
        print("user is already logged in")
        return redirect('/')

    context = {}
    context['form'] = RegistrationForm()
    return render(request, "register.html", context)


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
            user.avatar = form.cleaned_data['avatar']

            #password and confirm password must match
            if user.password == user.confirmPassword:
                try:
                    #hash password
                    user.password = make_password(user.password)
                    #register a user
                    messages.success(request, "New account created!")
                    user.save()
                    return redirect('/')
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
    return render(request, 'register.html', context)


def editUserProfile(request):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    user = User.objects.get(userId=request.user.userId)
    context = {}
    context['form'] = UserProfileForm(instance = user)
    return render(request, 'edituserprofile.html', context)


def updateUserProfile(request):
    user = User.objects.get(userId=request.user.userId)
    form = UserProfileForm(request.POST, instance = user)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'edituserprofile.html', context)


def loginPage(request):
    #logged in users must not access 
    if request.user.is_authenticated:
        print("user is already logged in")
        return redirect('/')

    context = {}
    context['form'] = LoginForm()
    return render(request, "login.html", context)


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


def logoutUser(request):
    messages.success(request, "You are logged out!")
    logout(request)
    return redirect('/')


def deleteUser(request):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/')

    #delete the currently logged in user
    user = User.objects.get(userId=request.user.userId)
    user.delete()
    return redirect('/')


def searchUsers(request):
    if request.method == "POST":
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)
        return render(request, 'searchResults.html', {'searched': searched, 'users': users})
    else:
        return render(request, 'searchResults.html', {})


# ----------------------------
#  Main Forum Post
# ----------------------------

def createMainPost(request):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = MainPostForm()
    return render(request, "createMainPost.html", context)

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
                return redirect('/')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    #login failed
    context['form'] = MainPostForm()
    return render(request, 'createMainPost.html', context)

def editMainPost(request, postId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    mainPost = MainPost.objects.get(postId=postId)
    context = {}
    context['form'] = MainPostForm(instance = mainPost)
    return render(request, 'editMainPost.html', context)

def updateMainPost(request, postId):
    mainPost = MainPost.objects.get(postId=postId)
    form = MainPostForm(request.POST, instance=mainPost)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'editMainPost.html', context)

def deleteMainPost(request, postId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/')

    #delete the currently logged in user
    mainPost = MainPost.objects.get(postId=postId)
    mainPost.delete()
    return redirect('/')


# ----------------------------
#  Main Forum Post Comment
# ----------------------------

def createMainComment(request, postId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = MainCommentForm()
    return render(request, "createMainComment.html", context)

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
                return redirect('/')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    #login failed
    context['form'] = MainCommentForm()
    return render(request, 'createMainComment.html', context)

def editMainComment(request, commentId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    mainComment = MainComment.objects.get(commentId=commentId)
    context = {}
    context['form'] = MainCommentForm(instance = mainComment)
    return render(request, 'editMainComment.html', context)

def updateMainComment(request, commentId):
    mainComment = MainComment.objects.get(commentId=commentId)
    form = MainCommentForm(request.POST, instance=mainComment)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        messages.error(request, "Invalid form data")
    context['form'] = form
    return render(request, 'editMainComment.html', context)

def deleteMainComment(request, commentId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/')

    #delete the currently logged in user
    mainComment = MainComment.objects.get(commentId=commentId)
    mainComment.delete()
    return redirect('/')


# ----------------------------
#  Study Group
# ----------------------------

def createStudyGroup(request):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You need to log in to create a study group")
        return redirect('/login')

    context = {}
    context['form'] = StudyGroupForm()
    return render(request, "createStudyGroup.html", context)

def execCreateStudyGroup(request):
    context = {}
    if request.method == "POST":
        form = StudyGroupForm(request.POST)
        if form.is_valid():
            studyGroup = StudyGroup()
            studyGroup.groupName = form.cleaned_data['groupName']
            studyGroup.description = form.cleaned_data['description']
            #owner is the currently logged in user
            studyGroup.ownerId = User.objects.get(userId=request.user.userId)
            try:
                messages.success(request, "New study group created")
                studyGroup.save()
                return redirect('/')
            except:
                pass
        else:
            messages.error(request, "Invalid form data")

    #login failed
    context['form'] = StudyGroupForm()
    return render(request, 'createStudyGroup.html', context)

def editStudyGroup(request, studyGroupId):
    #not logged in users must not access 
    if not request.user.is_authenticated:
        messages.error(request, "You're not logged in")
        return redirect('/login')

    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    context = {}
    context['form'] = StudyGroupForm(instance = studygroup)
    return render(request, 'editStudyGroup.html', context)

def updateStudyGroup(request, studyGroupId):
    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    form = StudyGroupForm(request.POST, instance=studygroup)
    if form.is_valid():
        form.save()
        return redirect('/')
    else:
        messages.error(request, "Invalid form data")
    context = {}
    context['form'] = form
    return render(request, 'editStudyGroup.html', context)

def deleteStudyGroup(request, studyGroupId):
    #logged in users must not access 
    if not request.user.is_authenticated:
        print("You're not logged in")
        return redirect('/')

    #delete the currently logged in user
    studygroup = StudyGroup.objects.get(studyGroupId=studyGroupId)
    studygroup.delete()
    return redirect('/')

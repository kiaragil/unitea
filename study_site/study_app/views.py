from django.shortcuts import render, redirect
from django.template import loader
from study_app.forms import *
from study_app.models import *
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout

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


def aboutMember(request, member):
    template = loader.get_template('about/T4TM-{name}.html'.format(name=member))
    context = {}
    return HttpResponse(template.render(context, request))


# ----------------------------
#  User
# ----------------------------

def register(request):
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
                    user.save()
                    return redirect('/')
                except:
                    pass
            else:
                print("Confirm password doesn't match")
                context['form'] = form
        else:
            print("Invalid form data")
            context['form'] = form
    else:
        context['form'] = RegistrationForm()
    return render(request, 'register.html', context)


def loginPage(request):
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
            print(user)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                print("Authentication failed")
                context['form'] = form
        else:
            print("Invalid form data")
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')


def searchUsers(request):
    if request.method == "POST":
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)
        return render(request, 'searchResults.html', {'searched': searched, 'users': users})
    else:
        return render(request, 'searchResults.html', {})


# ----------------------------
#  Study Group
# ----------------------------

def createStudyGroup(request):
    context = {}
    context['form'] = StudyGroupForm()
    return render(request, "studygroupcreation.html", context)

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
            print(studyGroup.ownerId)
            try:
                studyGroup.save()
                return redirect('/')
            except:
                pass
        else:
            print("Invalid form data")

    #login failed
    context['form'] = StudyGroupForm()
    return render(request, 'studygroupcreation.html', context)


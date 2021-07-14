from django.shortcuts import render, redirect
from django.template import loader
from study_app.forms import RegistrationForm
from study_app.models import User
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})

def contactus(request):
    return render(request, 'contactus.html')

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
            if user.password == user.confirmPassword:
                try:
                    user.password = make_password(user.password)
                    user.save()
                    return redirect('/')
                except:
                    pass
            else:
                print("Confirm password doesn't match")
                context['form'] = form
        else:
            print("Form not valid")
            context['form'] = form
    else:
        context['form'] = RegistrationForm()
    return render(request, 'register.html', context)

def searchUsers(request):
    if request.method == "POST":
        searched = request.POST['searched']
        users = User.objects.filter(username__contains=searched)
        return render(request, 'searchResults.html', {'searched': searched, 'users': users})
    else:
        return render(request, 'searchResults.html', {})

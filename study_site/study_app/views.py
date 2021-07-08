from django.shortcuts import render, redirect
from django.template import loader
from study_app.forms import RegistrationForm
from study_app.models import User
from django.http import HttpResponse


# Create your views here.
def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})


def searchresults(request):
    return render(request, 'searchresults.html')


def contactus(request):
    return render(request, 'contactus.html')

def construction(request):
    return render(request, 'construction.html')


def register(request):
    return render(request, 'register.html')


def about(request):
    return render(request, 'about.html')

def kiara(request):
    return render(request, 'T4TM-Kiara.html')


def ostyn(request):
    return render(request, 'T4TM-Ostyn.html')


def josh(request):
    return render(request, 'T4TM-Josh.html')


def miho(request):
    return render(request, 'T4TM-Miho.html')


def vernon(request):
    return render(request, 'T4TM-Vernon.html')


def cong(request):
    return render(request, 'T4TM-Cong.html')


def melinda(request):
    return render(request, 'T4TM-Melinda.html')


def register(request):
    context = {}
    context['form'] = RegistrationForm()
    return render(request, "register.html", context)


def createUser(request):
    context = {}
    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            try:
                form.save()
                return redirect('/home')
            except:
                pass
        else:
            print("Form not valid")
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




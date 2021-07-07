from django.shortcuts import render
# Create your views here.
def index(request):
    return render(request,'index.html')

def searchresults(request):
    return render(request, 'searchresults.html')


def contactus(request):
    return render(request, 'contactus.html')


def register(request):
    return render(request, 'register.html')


def about(request):
    return render(request, 'about.html')

def kiara(request):
    return render(request,'T4TM-Kiara.html')
    
def ostyn(request):
    return render(request,'T4TM-Ostyn.html')

def josh(request):
    return render(request,'T4TM-Josh.html')

def miho(request):
    return render(request,'T4TM-Miho.html')

def vernon(request):
    return render(request,'T4TM-Vernon.html')

def cong(request):
    return render(request,'T4TM-Cong.html')

def melinda(request):
    return render(request,'T4TM-Melinda.html')
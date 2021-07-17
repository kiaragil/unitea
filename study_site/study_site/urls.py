"""study_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from study_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('about', views.about),
    path('about/<str:member>', views.aboutUs),

    path('register', views.register),
    path('createuser', views.createUser),
    path('edituser', views.editUserProfile),
    path('updateuser', views.updateUserProfile),
    path('login', views.loginPage),
    path('loginaccount', views.loginUser),
    path('logout', views.logoutUser),
    path('deleteuser', views.deleteUser),
    path('searchusers', views.searchUsers),
    
    path('contactus', views.contactusPage),
    path('submitcontactus', views.submitContactus),
    
    path('createstudygroup', views.createStudyGroup),
    path('execcreatestudygroup', views.execCreateStudyGroup),
    path('<int:id>/editstudygroup', views.editStudyGroup),
    path('<int:id>/updatestudygroup', views.updateStudyGroup),
    path('<int:id>/deletestudygroup', views.deleteStudyGroup),
    
    path('construction', views.construction),
    path('landing', views.landing)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

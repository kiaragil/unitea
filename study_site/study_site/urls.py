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
    path('home', views.home),
    path('about', views.about),
    path('landing', views.landing),

    path('register', views.register, name='register'),
    path('createuser', views.createUser),
    path('edituser', views.editUserProfile),
    path('updateuser', views.updateUserProfile),
    path('login', views.loginPage, name='login'),
    path('loginaccount', views.loginUser),
    path('logout', views.logoutUser),
    path('deleteuser', views.deleteUser),
    path('confirmdeleteuser', views.confirmDeleteUser),
    path('search', views.searchStudyGroups),
    path('editpassword', views.editPassword),
    path('updatepassword', views.updatePassword),
    path('termsofservice', views.tos),

    path('<int:userId>/userprofile', views.showUserProfile),
    
    path('contactus', views.contactusPage),
    path('submitcontactus', views.submitContactus),
    path('report', views.report),

    path('FAQ', views.FAQ),
    
    path('mainforum', views.showMainForum),
    
    path('createmainpost', views.createMainPost),
    path('execcreatemainpost', views.execCreateMainPost),
    path('<int:postId>/mainpost', views.showMainPost),
    path('<int:postId>/editmainpost', views.editMainPost),
    path('<int:postId>/updatemainpost', views.updateMainPost),
    path('<int:postId>/deletemainpost', views.deleteMainPost),

    path('<int:postId>/execcreatemaincomment', views.execCreateMainComment),
    path('<int:postId>/<int:commentId>/editmaincomment', views.editMainComment),
    path('<int:postId>/<int:commentId>/updatemaincomment', views.updateMainComment),
    path('<int:postId>/<int:commentId>/deletemaincomment', views.deleteMainComment),
    
    path('userStudyGroupListing', views.userStudyGroupListing),
    path('<str:subject>/studygrouplisting', views.showStudyGroupListing),

    path('createstudygroup', views.createStudyGroup),
    path('execcreatestudygroup', views.execCreateStudyGroup),
    path('<int:studyGroupId>/studygroup', views.showStudyGroup),
    path('<int:studyGroupId>/joinstudygroup', views.joinStudyGroup),
    path('<int:studyGroupId>/leavestudygroup', views.leaveStudyGroup),
    path('<int:studyGroupId>/editstudygroup', views.editStudyGroup),
    path('<int:studyGroupId>/updatestudygroup', views.updateStudyGroup),
    path('<int:studyGroupId>/deletestudygroup', views.deleteStudyGroup),

    path('<int:studyGroupId>/createstudygrouppost', views.createStudyGroupPost),
    path('<int:studyGroupId>/execcreatestudygrouppost', views.execCreateStudyGroupPost),
    path('<int:studyGroupId>/<int:postId>/studygrouppost', views.showStudyGroupPost),
    path('<int:studyGroupId>/<int:postId>/editstudygrouppost', views.editStudyGroupPost),
    path('<int:studyGroupId>/<int:postId>/updatestudygrouppost', views.updateStudyGroupPost),
    path('<int:studyGroupId>/<int:postId>/deletestudygrouppost', views.deleteStudyGroupPost),

    path('<int:studyGroupId>/<int:postId>/execcreatestudygroupcomment', views.execCreateStudyGroupComment),
    path('<int:studyGroupId>/<int:postId>/<int:commentId>/editstudygroupcomment', views.editStudyGroupComment),
    path('<int:studyGroupId>/<int:postId>/<int:commentId>/updatestudygroupcomment', views.updateStudyGroupComment),
    path('<int:studyGroupId>/<int:postId>/<int:commentId>/deletestudygroupcomment', views.deleteStudyGroupComment),

    path('construction', views.construction),
    

    # ----------------------------
    #  Front End Testing 
    # ----------------------------
    # path('testEditStudyGroup', views.testEditStudyGroup),
    # path('testCreateStudyPost', views.testCreateStudyPost),
    # path('testCreateMainPost', views.testCreateMainPost),
    # path('testEditMainPost', views.testEditMainPost),
    # path('testEditStudyGroupPost', views.testEditStudyGroupPost),
    # path('testUserProfile', views.testUserProfile),
    # path('testEditUserProfile', views.testEditUserProfile),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

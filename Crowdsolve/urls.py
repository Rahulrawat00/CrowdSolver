"""
URL configuration for Crowdsolve project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from CrowdSolver import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('' , views.home , name='home'),
    path('', views.admindashboard, name='admindashboard'),
    path('membersignup/', views.MemberSignup, name='membersignup'),
    path('verifymember/' , views.verifymember  , name='verifymember'),

    path('issuereport/', views.issuereport, name='issuereport'),
  
    path('ticketraise/', views.addIssue , name= 'ticketraise'),
    path('notification/' , views.notification, name='notification'),
    path('approve-solution/<int:solution_id>/', views.approve_solution, name='approve_solution'),
    path('voting/', views.voting, name='voting'),
    path('clear-selected-user/', views.clear_selected_user, name='clear_selected_user'),
    path('memberlogin/', views.memberlogin, name='memberlogin'),
    path('memberlogout/', views.memberlogout, name='memberlogout'),
    path('secretarylogin/', views.secretary_login, name='secretarylogin'),
    path('secretaryotp/', views.secretary_otp_verify, name='secretaryotp'),
    path('solutions/<int:issue_id>/' , views.issue_solution, name='solutions'),
    path('viewSolutions/', views.view_solutions , name='viewSolutions'),
    # path('pendingvotes', views.member_count, name='pendingvotes'),
    

   

    

    
 
    

]

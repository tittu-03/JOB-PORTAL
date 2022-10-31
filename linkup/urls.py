"""job_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from django.urls import path
from .views import *
from linkup import views

urlpatterns = [

    path('',home,name='home'),
    path('company_reg/',company_reg,name='company_reg'),
    path('company_login/',company_login,name='company_login'),
    path('verify/<auth_token>',views.verify),
    path('error/',views.error),
    path('tockensend/',views.tokensend),
    path('success/',views.success),
    path('company_pro/',views.company_pro),
    path('edit_company_profile/<str:token>/<str:email>',company_profile_edit),
    path('showoff/',views.show),
    path('userreg/',views.user_reg),
    path('userlogin/',views.user_login),
    path('post_job/',views.post_job),
    path('show_job/',show_job),
    path('job_details/<int:id>',job_details),
    path('user_pro/',user_pro),
    path('apply_job/<str:title>/<str:company_name>',apply),
    path('view_applicants/<str:jobtitle>/<str:companyname>',view_applicants),
    path('jobs_posted_by_company/<str:by>',jobs_posted_by_company),
    path('view_applied_jobs/<str:mail>',view_applied_jobs),


]
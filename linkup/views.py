from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from .forms import *
from .models import *
from django.core.mail import send_mail
from job_portal.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from django.conf import settings
from django.contrib.auth import authenticate


# Create your views here.
def home(request):
    return render(request, 'home.html')


def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request, 'user not found')
            return redirect(company_login)
        profile_obj = profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request, 'profile not verified plz check your email')
            return redirect(company_login)
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'wrong password or username')
            return redirect(company_login)
        company=profile.objects.filter(user=user)
        return render(request,'company_pro.html',{'profile':company})
    return render(request, 'company_login.html')


def company_reg(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        # phone=request.POST.get('phone')
        password1=request.POST.get('password1')
        if password == password1:
            if User.objects.filter(username=username).first():
                messages.success(request,'username already taken')
                return redirect('/company_reg/')
            if User.objects.filter(email=email).first():
                messages.success(request,'email already exist')
                return redirect('/company_reg/')
            user_obj=User(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
            profile_obj.save()
            send_mail_regis(email,auth_token)
            return redirect (tokensend)
        else :
            messages.success(request, 'Password Mismatch')

    return render(request, 'company_reg.html')

def send_mail_regis(email,token):
    subject='your account has been verified'
    message=f'past the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(company_login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'Your account has been verified')
        return redirect(success)
    else:
        return redirect('/error')

def success(request):
    return render(request,'success.html')

def tokensend(request):
    return render(request,'tockensend.html')

def error(request):
    return render(request,'errorpage.html')

def company_pro(request):
    return render(request,'company_pro.html')

def company_profile_edit(request,token,email):
    if request.method=='POST':
        a=User.objects.filter(email=email).first()
        a.username=request.POST.get('username')
        a.email=request.POST.get('email')
        a.save()
        company=profile.objects.filter(auth_token=token)
        return render(request,'company_pro.html',{'profile':company})
    x=profile.objects.get(auth_token=token)
    return render(request,'edit_company_pro.html',{'value':x})

def show(request):
    a=profile.objects.all()
    return render(request,'showoff.html',{'i':a})

def user_reg(request):
    if request.method=='POST':
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password1=request.POST.get('password1')
        if password==password1:
            if User.objects.filter(username=username).first():
                messages.success(request,'username is already taken')
                return render(request,'user_reg.html')
            if User.objects.filter(email=email).first():
                messages.success(request,'Email IS Already Exist')
                return render(request,'user_reg.html')
            user_object=User(username=username,email=email,first_name=firstname,last_name=lastname)
            user_object.set_password(password)
            user_object.save()
            profile=User.objects.filter(username=user_object)
            return render(request,'user_pro.html',{'x':profile})
        else:
            messages.success(request,'Password Mismatch')
            return render(request,'user_reg.html')
    return render(request,'user_reg.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        a=User.objects.filter(username=username).first()
        if a is None:
            messages.success(request,'user not found')
            return redirect(user_login)
        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'wrong Usernname or password')
            return redirect(user_login)
        profile = User.objects.filter(username=username)
        return render(request, 'user_pro.html', {'x': profile})
    return render(request,'user_login.html')

def post_job(request):
    if request.method=='POST':
        a=postjobform(request.POST)
        if a.is_valid():
            companyname=a.cleaned_data['companyname']
            jobtitle=a.cleaned_data['jobtitle']
            wtype=a.cleaned_data['wtype']
            jtype=a.cleaned_data['jtype']
            experience=a.cleaned_data['experience']
            description=a.cleaned_data['description']
            b=postjobmodel(jobtitle=jobtitle,companyname=companyname,wtype=wtype,jtype=jtype,experience=experience,description=description)
            b.save()
            return HttpResponse('success')
    return render(request,'post_job.html')

def show_job(request):
    a=postjobmodel.objects.all()
    return render(request,'show_job.html',{'i':a})

def job_details(request,id):
    a=postjobmodel.objects.filter(id=id)
    return render(request,'job_details.html',{'x':a})

def user_pro(request):
    return render(request,'user_pro.html')

def apply(request,title,company_name):
    if request.method=='POST':
        full_name=request.POST.get('fullname')
        email=request.POST.get('email')
        country_code=request.POST.get('country_code')
        phone=request.POST.get('phone')

        resume=request.FILES['resume']

        current_position=request.POST.get('current_position')
        current_company=request.POST.get('current_company')


        title=title
        cmp_name=company_name

        a=apply_job.objects.create(full_name=full_name,email=email,phone=phone,country_code=country_code,resume=resume,current_position=current_position,current_company=current_company,job_title=title,company_name=cmp_name)
        a.save()
        profile = User.objects.filter(email=email)
        messages.success(request,'applied succesfully')
        return render(request, 'user_pro.html', {'x': profile})


    return render(request,'apply_job.html')

def jobs_posted_by_company(request,by):
    a=postjobmodel.objects.filter(companyname=by)
    return render(request,'posted_jobs.html',{'job':a})

def view_applicants(request,jobtitle,companyname):
    a=apply_job.objects.filter(job_title=jobtitle,company_name=companyname)
    li=[]
    for i in a:
        path=i.resume
        li.append(str(path).split('/')[-1])
    context=zip(a,li)
    return render(request,'applicants_view.html',{'x':context})

def view_applied_jobs(request,mail):
    a=apply_job.objects.filter(email=mail)
    return render(request, 'applied_jobs.html', {'x':a})

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    # phone = models.IntegerField()
    def __str__(self):
        return self.user.username

class user(models.Model):
    username=models.OneToOneField(User,on_delete=models.CASCADE)

class postjobmodel(models.Model):
    worktype=[
        ('remote','remote'),
        ('hybrid','hybrid')
    ]
    jobtype=[
        ('parttime','parttime'),
        ('fulltime','fulltime')
    ]

    exp=[
        ('0-1','0-1'),
        ('1-2','1-2'),
        ('2-3','2-3'),
        ('3-4','3-4'),
        ('4-5','4-5'),
        ('5-6','5-6'),
        ('6-7','6-7'),
        ('7-8','7-8'),
        ('8-9','8-9'),
        ('9+ years','9+ years')
    ]
    companyname=models.CharField(max_length=30)
    jobtitle=models.CharField(max_length=50)
    wtype=models.CharField(max_length=30,choices=worktype)
    jtype=models.CharField(max_length=30,choices=jobtype)
    experience=models.CharField(max_length=30,choices=exp)
    description=models.CharField(max_length=300)

class apply_job(models.Model):
    code = [
        ('+91', '+91'),
        ('+99', '+99'),
        ('+90', '+90'),
        ('+66', '+66')
    ]

    full_name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.IntegerField()
    country_code=models.IntegerField(choices=code)
    resume=models.FileField( upload_to='linkup/static',default="")
    current_position=models.CharField(max_length=100,default="")
    current_company=models.CharField(max_length=100,default="")
    date=models.DateField(auto_now_add=True)
    job_title=models.CharField(max_length=50,default="")
    company_name=models.CharField(max_length=100,default="")

    def _str_(self):
        return self.email
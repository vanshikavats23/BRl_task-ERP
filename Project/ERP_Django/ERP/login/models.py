from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


#creating an base user
class UserManager(BaseUserManager):
    def create_user(self,id,password=None,**extra_fields):
        if not id:
            raise ValueError('the id filed must be set')
        if not password:
            raise ValueError('set password')
        user=self.model(id=id,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
#creating an super user

    def create_superuser(self,id,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("speruser must have is_staff=true.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser must have is_superuser=True")
        
        return self.create_user(id,password,**extra_fields)
    

#creating a login database   
class LoginUser(AbstractBaseUser):
    user_id=models.IntegerField(unique=True)
    password=models.CharField(max_length=100)
    is_verified=models.BooleanField(default=False)
    otp=models.IntegerField(null=True,blank=True)

    objects=UserManager
    USERNAME_FIELD='id'
    REQUIRED_FIELDS=[id]

    def __str__(self):
        return self.id



class Student(models.Model):
    user_id=models.IntegerField(unique=True)
    password=models.CharField(max_length=100,default='1234')
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone_number=models.IntegerField(unique=True)
    profile_photo_url=models.URLField()
    role=models.CharField(max_length=100,default='student')
    Branch=models.CharField(max_length=100)
    Year=models.IntegerField()
    semester=models.IntegerField()
    section=models.CharField(max_length=100)
    objects=UserManager
    USERNAME_FIELD='id'
    REQUIRED_FIELDS=[id]

    def __str__(self):
        return self.id
    
class Faculty(models.Model):
    user_id=models.IntegerField(unique=True)
    password=models.CharField(max_length=100,default='1234')
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    phone_number=models.IntegerField(unique=True)
    profile_photo_url=models.URLField()
    role=models.CharField(max_length=100,default='faculty')
    Post=models.CharField(max_length=100)
    Department=models.CharField(max_length=100)
    objects=UserManager
    USERNAME_FIELD='id'
    REQUIRED_FIELDS=[id]

    def __str__(self):
        return self.id    
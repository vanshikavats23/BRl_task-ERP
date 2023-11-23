from django.contrib import admin
from django.urls import path,include
from .views import register,dataeditor,VerifyOTP,PasswordResetRequest,PasswordReset

urlpatterns = [
    path('register/',register.as_view(),name='register'),
    path('dataeditor/',dataeditor.as_view(),name='dataeditor'),
    path("verifyotp/",VerifyOTP.as_view(),name="verifyotp"),
    path("passwordreset/",PasswordResetRequest.as_view(),name="passwordresetrequest"),
    path("password/reset/<str:token>/",PasswordReset.as_view(),name="passwordreset"),]
    
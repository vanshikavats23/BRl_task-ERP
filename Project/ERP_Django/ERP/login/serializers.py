
from rest_framework import serializers
from  .models import LoginUser,Student,Faculty

class LoginSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    password = serializers.CharField(write_only=True)


class UserSerialiazer(serializers.ModelSerializer):
    class Meta:
        model=LoginUser
        fields=['user_id','password','is_verified']

class dataeditorserializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['user_id','first_name','last_name','email','phone_number','role','Branch','Year','semester','section','password']        

    
class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()
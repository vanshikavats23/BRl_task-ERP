""" 
import jwt
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import LoginSerializer

SECRET_KEY = 'your-secret-key'

def generate_jwt_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.validated_data['id']
    password = serializer.validated_data['password']

    user = authenticate(request, username=user_id, password=password)

    if user is not None:
        auth_login(request, user)
        token = generate_jwt_token(user_id=user_id, username=user.username, role='student')
        return Response({'token': token})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

@api_view(['POST'])
def custom_logout(request):
    auth_logout(request)
    return Response({'message': 'Logout successful'})

 """

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from .emails import send_otp_via_email,generate_jwt_token


class dataeditor(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=dataeditorserializer(data=data)
            if serializers.is_valid():
                serializers.save()
                return Response({
                    'status':200,
                    'message':'data created',
                    'data':serializers.data,
                })
            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializers.errors,
            })   
        
        except Exception as e:
            print(e)




class register(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=UserSerialiazer(data=data)
            if serializers.is_valid():
                user_id = serializers.validated_data['user_id']
                password = serializers.validated_data['password']
                
                print(user_id,password)
                #Check if user_id is in Student model
                student = Student.objects.filter(user_id=user_id).first()
                # If not found in Student model, check in Teacher model
                if not student:
                    faculty = Faculty.objects.filter(user_id=user_id).first()
                    if not faculty:
                        return Response({'error': 'User not found'}, status=404)
                    user = faculty
                else:
                    user = student

                if user.password == password:
                    email=user.email
                    send_otp_via_email(email,user_id,password)
                    return Response({'message': 'OTP sent to email'})

                else:
                    return Response({'error': 'Invalid credentials'}, status=401)    
    

            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializers.errors,
            })   
        
        except Exception as e:
            print(e)


class VerifyOTP(APIView):
    def post(self,request):
        try:
            data=request.data
            serializers=VerifyOTPSerializer(data=data)
            if serializers.is_valid():
                otp=serializers.validated_data['otp']
                email=serializers.validated_data['email']
                #checking in loginuser model
                user=LoginUser.objects.filter(otp=otp).first()
                
                if user:
                    
                    #fetching user_id form student/Faculty model
                    student = Student.objects.filter(email=email).first()
                    if not student:
                        faculty = Faculty.objects.filter(email=email).first()
                        if not faculty:
                            return Response({'error': 'User not found'}, status=404)
                        user_ = faculty
                    else:
                        user_ = student
                    user_id=user_.user_id    
                    role=user_.role
                    
                    user.is_verified=True
                    user.save()
                    user.delete()
                    return Response({'message': 'OTP verified successfully',
                                     'token': generate_jwt_token(user_id=user_id, role=role)})
                else:
                    return Response({'error': 'Invalid OTP'}, status=401)
            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializers.errors,
            })    

        except Exception as e:
            print(e)    

        

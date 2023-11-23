

""" @api_view(['POST'])
def custom_logout(request):
    auth_logout(request)
    return Response({'message': 'Logout successful'}) """

 

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from .emails import send_otp_via_email,generate_jwt_token,send_passwordreset_mail,decode_jwt_token_reset


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



from django.http import HttpResponse
from django.middleware.csrf import rotate_token

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
                    token=generate_jwt_token(user_id=user_id, role=role)
                    user.is_verified=True
                    user.save()
                    user.delete()

                    #cokkie setting
                    response = Response({'user_id': user_id, 'otp_sent': True, 'token': token}, status=200)
                    response.set_cookie('jwt_token', token, httponly=True, secure=True)  # Use secure=True in production with HTTPS
                    return response
                else:
                    return Response({'error': 'Invalid OTP'}, status=401)
            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializers.errors,
            })    

        except Exception as e:
            print(e)    

        
class PasswordResetRequest(APIView):
    def post(self, request):
        try:
            data = request.data
            serializers = PasswordResetSerializer(data=data)

            if serializers.is_valid():
                email = serializers.validated_data.get('email')

                student_user = Student.objects.filter(email=email).first()
                faculty_user = Faculty.objects.filter(email=email).first()

                if not student_user and not faculty_user:
                    return Response({'error': 'User not found: unauthorized email'}, status=404)

                # Assuming you have a function to send password reset mail
                print(email)
                send_passwordreset_mail(email)

                return Response({'message': 'Password reset link sent to email'})

            return Response({'error': 'Invalid data'}, status=400)

        except Exception as e:
            print(e)
            # Handle other exceptions as needed
            return Response({'error': 'Internal Server Error'}, status=500)    
        

used_tokens = {}
#token is sent in url and new password is taken from user        
class PasswordReset(APIView):
            def post(self, request,token):
                 
                #token= request.query_params.get('token', None)
        
                if token is None:
                    return Response({'error': 'token is required'}, status=400)      # Handle the case where 'email' is not provided
                
                # Check if the token has already been used
                if used_tokens.get(token):
                    return Response({'error': 'Token has already been used'}, status=400)
                
                email=decode_jwt_token_reset(token)
            
                if email is None:
                    return Response({'error': 'Invalid token'}, status=401)
                student=Student.objects.filter(email=email).first()
                if student is None:
                    faculty=Faculty.objects.filter(email=email).first()
                    if faculty is None:
                        return Response({'error': 'User not found'}, status=404)
                    user=faculty
                else:
                    user=student
                
                serializers = PasswordtakingSerializer(data=request.data)
                if serializers.is_valid():
                    password= serializers.validated_data.get('password')
                    confirm_password= serializers.validated_data.get('confirm_password')

                    if password != confirm_password:
                        return Response({'error': 'Passwords do not match'}, status=400)
                    user.password=password
                    user.save()
                    used_tokens[token] = True
                    
                    return Response({'message': 'Password reset successful'})
                else:
                    return Response(serializers.errors,status=400)    

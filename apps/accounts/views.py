from django.shortcuts import render
from rest_framework import generics,status
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from apps.analytics.models import *
from datetime import datetime
from django.core import signing
from django.utils.timezone import now, timedelta
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from .models import Account as  User
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from apps.tickets.models import Ticket






class ClientSignup(APIView):
    authentication_classes=[]
    permission_classes=[]

    def post(self, request):
        serializer = SignupSerializers(data=request.data)
        if serializer.is_valid():
                user = serializer.save()
                token = Token.objects.create(user=user)
                if (user.account_type=="Facteur")or(user.account_type=="Employee"):
                    Employee_data.objects.create(employee = user)
            
                return Response({"message": "Client account created.","Token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    authentication_classes = []  # Disable default authentication for this view
    permission_classes = []  # Open to all users

    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            username = serializer.validated_data.get("username")
            password = serializer.validated_data["password"]

            if email:
                # Authenticate using email
                user = authenticate(username=email, password=password)
                if user:
                 try:
                    ticket = Ticket.objects.get(owner=user)
                    if ticket:
                     token, _ = Token.objects.get_or_create(user=user)
                     return Response(
                        {"message": "Logged in successfully", "token": token.key,"has_ticket":True},
                        status=status.HTTP_200_OK
                    )
                 except:

                     token, _ = Token.objects.get_or_create(user=user)
                     return Response(
                        {"message": "Logged in successfully", "token": token.key,"has_ticket":False},
                        status=status.HTTP_200_OK
                    )                        
                else:
                    return Response(
                        {"message": "Invalid email or password"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

            elif username:
                # Authenticate using username
                user = authenticate(username=username, password=password)
                if user:
                    
                    login(request, user)
                    analysis = Employee_data.objects.get(employee = user)
                    analysis.todayLogin = datetime.now()
                    if user.is_superuser:
                        superuser = True
                    else:
                        superuser = False

                    return Response(
                        {"message": "Logged in successfully with session",
                         "is_admin": superuser},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"message": "Invalid username or password"},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Define a salt for signing
SALT = "reset-password-salt"

# Expiry time in minutes
EXPIRY_TIME = 5

def generate_signed_url(email):
    timestamp = now().timestamp()
    data = {'email': email, 'timestamp': timestamp}
    signed_data = signing.dumps(data, salt=SALT)
    return signed_data

def validate_signed_url(signed_data):
    try:
        data = signing.loads(signed_data, salt=SALT)
        email = data['email']
        timestamp = data['timestamp']
        if now().timestamp() - timestamp > EXPIRY_TIME * 60:
            return None, "Link expired"
        return email, None
    except signing.BadSignature:
        return None, "Invalid or tampered link"





class SendResetLinkView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        
        # Ensure email is provided
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        
            # Retrieve the user by email
        user = User.objects.get(email=email)

            # Generate reset code (you might want to hash it or use a more secure approach)
        reset_code = random.randint(1000, 9999)

            # Save the reset code to the user object (be sure to save the user object)
        user.reset_code = reset_code
        user.save()

            # Send the reset code via email
        send_mail(
                'Password Reset Link',
                f'Your password reset code is: {reset_code}',
                '7arfa2024@gmail.com',
                [email],
                fail_silently=False,
            )

            # Generate the reset link (use a URL-safe format if you're using a signed URL)
        signed_data = generate_signed_url(email)  # This should generate a signed URL safely
        reset_link = f"/reset-password/validate-code/{signed_data}/"
            
        return Response({
                'message': 'Reset link sent to your email',
                'reset_link': reset_link  # Corrected response format
            }, status=status.HTTP_200_OK)






class ValidateResetCodeView(APIView):
    authentication_classes=[]
    permission_classes= []
    def post(self, request, signed_data):
        email, error = validate_signed_url(signed_data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        reset_code = request.data.get('reset_code')
        try:
            user = User.objects.get(email=email, reset_code=reset_code)
            return Response({'message': 'Code is valid'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, signed_data):
        email, error = validate_signed_url(signed_data)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.reset_code = None  
            user.save()
            return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)


              

from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import  Token
from rest_framework import status
from .serializers import UserSerializer

import pyotp
import qrcode
from io import BytesIO
import base64

@api_view(['POST'])
def register_api(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(**serializer.data)
        token = Token.objects.create(user=user)
        return Response({
            "message": "User registered successfully",
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Set up 2FA by generating a TOTP secret and returning a QR code
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def setup_2fa(request):
    user = request.user
    profile = user
    if not profile.totp_secret:
        totp_secret = pyotp.random_base32()  # Generate a new TOTP secret
        profile.totp_secret = totp_secret
        profile.save()
    else:
        totp_secret = profile.totp_secret

    totp = pyotp.TOTP(totp_secret)
    otp_auth_url = totp.provisioning_uri(name=user.email, issuer_name="setup")

    # Generate QR code for the TOTP secret
    qr = qrcode.make(otp_auth_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_code_image = base64.b64encode(buffer.getvalue()).decode()

    return Response({
        'qr_code_image': f"data:image/png;base64,{qr_code_image}",
        'totp_secret': totp_secret,
    })

# Verify the OTP entered by the user
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_2fa(request):
    otp = request.data.get('otp')
    user = request.user
    profile = user.userprofile

    if not profile.totp_secret:
        return Response({"error": "2FA is not enabled for this user."}, status=status.HTTP_400_BAD_REQUEST)

    totp = pyotp.TOTP(profile.totp_secret)

    if totp.verify(otp):
        # OTP verified successfully
        return Response({"message": "2FA verified successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)



def welcome(request):
    return render(request,'hello.html')

def user_list_view(request):
    users = User.objects.all()  # Fetch all registered users
    return render(request, 'user_list.html', {'users': users})

@api_view(['DELETE'])
def deluser(request):
    username = request.data.get('username')

    if not username:
        return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
# from rest_framework.response  import Response
# from rest_framework.decorators  import api_view
# from django.contrib.auth.models import User
# from rest_framework import status
# from django.shortcuts import render
# from django.contrib.auth import login , authenticate
# from django.http import HttpResponse
# from rest_framework_simplejwt.tokens import RefreshToken







# # # Create your views here.




# @api_view(['POST'])
# def signup(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     email = request.data.get('email')

#     if not username or not password or not email:
#         return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

#     if User.objects.filter(username=username).exists():
#         return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

#     user = User.objects.create_user(username=username, email=email, password=password)

#     return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


# @api_view(['POST'])
# def signin(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     if not username or not password:
#         return Response({"error":"Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#     user = authenticate(request, username=username, password=password)

#     if user is not None:
#         login(request, user)
#         refresh = RefreshToken.for_user(user)
#         response = Response({
#             "message": "User logged in successfully",
#             "access":str(refresh.access_token),
#         }, status=status.HTTP_200_OK)
#         response.set_cookie(key='refresh', value=str(refresh), httponly=True)
#         return response
#     else:
#         return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
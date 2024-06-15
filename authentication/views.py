from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import auth
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import UserProfile, AgencyUserSignup, ClientUserSignup
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from datetime import timedelta

@api_view(["GET"])
def index(request):
    return Response({"message": "Hello there from api"})

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# @api_view(["POST", "GET"])
# def registerAgencyUser(request):
#     username = request.data.get("username")
#     email = request.data.get("email")
#     password = request.data.get("password")
#     user_img  = request.FILES.get("userProfileImg")

#     new_user = User.objects.create_user(username=username, email=email, password=password)
#     new_user.save()

#     new_agency_user_profile = AgencyUserSignup.objects.create(user=new_user, agency_profile_img=user_img)
#     new_agency_user_profile.save()

#     if new_user:
#         refresh = RefreshToken.for_user(new_user)
#         data = {
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh),
#             'user_id': new_user.id,
#             'username': new_user.username,
#             'email': new_user.email,
#         }

#         return Response({"user has been created": data}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Signup process has failed plz try again'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def registerAgencyUser(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    user_img  = request.FILES.get("userProfileImg")

    new_user = User.objects.create_user(username=username, email=email, password=password)
    new_user.save()

    new_agency_user_profile = AgencyUserSignup.objects.create(user=new_user, agency_profile_img=user_img)
    new_agency_user_profile.save()

    if new_user:
        refresh = RefreshToken.for_user(new_user)
        access_token = str(refresh.access_token)

        # Set access token as an HTTP-only cookie
        response = JsonResponse({"user has been created": "success", "access_token": access_token})
        response.set_cookie('access_token', access_token, max_age=3600, secure=True, httponly=True, samesite='None')
        return response
    else:
        return Response({'error': 'Signup process has failed plz try again'}, status=status.HTTP_401_UNAUTHORIZED)
    

# @api_view(["POST", "GET"])
# def registerClientUser(request):
#     username = request.data.get("username")
#     email = request.data.get("email")
#     password = request.data.get("password")
#     user_img  = request.FILES.get("userProfileImg")

#     new_user = User.objects.create_user(username=username, email=email, password=password)
#     new_user.save()

#     new_client_user_profile = ClientUserSignup.objects.create(user=new_user, client_profile_img=user_img)
#     new_client_user_profile.save()

#     if new_user:
#         refresh = RefreshToken.for_user(new_user)
#         data = {
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh),
#             'user_id': new_user.id,
#             'username': new_user.username,
#             'email': new_user.email,
#         }

#         return Response({"user has been created": data}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Signup process has failed plz try again'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(["POST", "GET"])
def registerClientUser(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    user_img  = request.FILES.get("userProfileImg")

    new_user = User.objects.create_user(username=username, email=email, password=password)
    new_user.save()

    new_client_user_profile = ClientUserSignup.objects.create(user=new_user, client_profile_img=user_img)
    new_client_user_profile.save()

    if new_user:
        refresh = RefreshToken.for_user(new_user)
        access_token = str(refresh.access_token)

        # Set access token as an HTTP-only cookie
        response = JsonResponse({"user has been loggedin": "success", "access_token": access_token})
        response.set_cookie('access_token', access_token, max_age=3600, secure=True, httponly=True, samesite='None')
        return response
    else:
        return Response({'error': 'Signin process has failed plz try again'}, status=status.HTTP_401_UNAUTHORIZED)
    

# @api_view(["POST"])
# def login_agency_user(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)

#     if user:
#         refresh = RefreshToken.for_user(user)
#         data = {
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh),
#             'user_id': user.id,
#             'username': user.username,
#             'email': user.email,
#         }

#         return Response(data, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def login_agency_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        # Set access token as an HTTP-only cookie
        response = JsonResponse({"login": "success", "access_token": access_token})
        response.set_cookie('access_token', access_token, max_age=3600, secure=True, httponly=True, samesite='None')
        return response
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
    
# @api_view(["POST"])
# def login_client_user(request):
#     username = request.data.get("username")
#     password = request.data.get("password")

#     user = authenticate(username=username, password=password)

#     if user:
#         refresh = RefreshToken.for_user(user)
#         data = {
#             'access_token': str(refresh.access_token),
#             'refresh_token': str(refresh),
#             'user_id': user.id,
#             'username': user.username,
#             'email': user.email,
#         }

#         return Response(data, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    
@api_view(["POST"])
def login_client_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = JsonResponse({"login": "success", "access_token": access_token})
        response.set_cookie('access_token', access_token, max_age=3600, secure=True, httponly=True, samesite='None')
        return response
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

# @api_view(["GET"])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def get_current_agency_user(request):
#     user_id = request.user.id if request.user else None
#     username = request.user.username if request.user else None
#     current_user_img = AgencyUserSignup.objects.get(user=request.user).agency_profile_img.url

#     context = {
#         "current user user": username,
#         "current user profile image": current_user_img,
#         "current users id": user_id
#     }

#     return Response(context)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_agency_user(request):
    user_id = request.user.id if request.user else None
    username = request.user.username if request.user else None
    cache_key = f"current_agency_user_{user_id}"

    # Attempt to retrieve the response from cache
    cached_response = cache.get(cache_key)
    if cached_response:
        return Response(cached_response)

    # If not cached, fetch from database
    try:
        current_user_img = AgencyUserSignup.objects.get(user=request.user).agency_profile_img.url
    except AgencyUserSignup.DoesNotExist:
        return Response({"error": "Agency user profile not found"}, status=status.HTTP_404_NOT_FOUND)

    context = {
        "current user user": username,
        "current user profile image": current_user_img,
        "current users id": user_id
    }

    cache.set(cache_key, context, timeout=3600)  # Cache for 1 hour (adjust timeout as needed)

    return Response(context)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_client_user(request):
    user_id = request.user.id if request.user else None
    username = request.user.username if request.user else None
    current_user_img = ClientUserSignup.objects.get(user=request.user).client_profile_img.url

    context = {
        "current user user": username,
        "current user profile image": current_user_img,
        "current users id": user_id
    }

    return Response(context)

# @api_view(['POST'])
# def refresh_token(request):
#     refresh = request.data.get('currentUserRefreshToken')
#     token = RefreshToken(refresh)

#     access_token = token.access_token
#     return Response({'access': str(access_token)})
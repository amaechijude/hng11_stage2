import json
import logging

from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, OrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.http.response import JsonResponse
from .models import Organisation

def index(request):
    context = {
        "hello": "hello"
    }
    return JsonResponse(context, safe=False)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        new_user = UserSerializer(data=request.data)
        if new_user.is_valid():
            # save new user
            user = new_user.save()

            # create organisation
            name = f"{user.firstName}'s Organistion"
            new_org = Organisation.objects.create(name=name)
            new_org.members.add(user)
            new_org.save()
            
            user_org = Organisation.objects.get(name=name)
            
            #tokens
            tokens = get_tokens_for_user(user)
            user_data = {
                    "status": "success",
                    "message": "Registration Successful",
                    
                    "data": {
                        #'refresh': tokens['refresh'],
                        'accessToken': tokens['access'],

                        'user': {
                            'userId': user.userId,
                            'firstName': user.firstName,
                            'lastName': user.lastName,
                            'email': user.email,
                            'phone': user.phone,
                            }
                        }
                    }
            return Response(user_data, status=status.HTTP_201_CREATED)
        
        result = {
            "status": "Bad Request",
            "message": "Registration unsuccessful",
            "statusCode": 400,
            "errors": new_user.errors
        }
        
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)

        output = {
            "status": "success",
            "message": "Login successful",
            
            "data": {
                # 'refresh': tokens['refresh'],
                'accessToken': tokens['access'],

                'user': {
                    'userId': user.userId,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'email': user.email,
                    'phone': user.phone,
                    }
                }
            }
        return Response(output, status=status.HTTP_200_OK)
    
    result = {
        "status": "Bad request",
        "message": "Authentication Failed",
        "statusCode": status.HTTP_401_UNAUTHORIZED
    }
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)



User = get_user_model()

@api_view(['GET'])
def user_detail(request, id):
    if request.user.is_authenticated:
        user = User.object.get(userId=id)

        if user == request.user or user.organisation.filter(members=request.user).exists():
            output = {
                    "status": "succes",
                    "message": f"Welcome {request.user.firstName}",

                    "data": {
                        'userId': user.userId,
                        'firstName': user.firstName,
                        'lastName': user.lastName,
                        'email': user.email,
                        'phone': user.phone,
                        }
                    }
            return Response(output, status=status.HTTP_200_OK)
        
        result = {
                "error" : "Unauthorised Access"
                }
        return Response(result, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET'])
def org_view(request):
    if request.user.is_authenticated:
        user = request.user
        all_org = user.organisation.all()
        serializer = OrganisationSerializer(data=all_org, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

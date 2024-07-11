import json
import logging

from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer, OrganisationSerializer, AddUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, permissions

from django.http.response import JsonResponse
from .models import Organisation



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
        user = User.objects.get(userId=id)

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



class org_view(generics.ListAPIView):
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        all_org = Organisation.objects.filter(members=user.userId)
        return all_org


class Org_details(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'orgId'

    def get(self, request, *args, **kwargs):
        try:
            org = self.get_object()
            if org.members.filter(userId=request.user.userId).exists():
                serializer = self.get_serializer(org)
                
                output = {
                    'status': 'success',
                    'message': 'Organisation retrieved successfully',
                    'data': serializer.data,
                    }
                return Response(output, status=status.HTTP_200_OK)
            
            payload = {
                'status': 'Forbidden',
                'message': 'You do not have permission to view this organisation',
                'statusCode': 403
                }
            return Response(payload, status=status.HTTP_403_FORBIDDEN)
        
        except Organisation.DoesNotExist:
            output = {
                'status': 'Not Found',
                'message': 'Organisation not found',
                'statusCode': 404
                }
            return Response(output, status=status.HTTP_404_NOT_FOUND)

     

@api_view(['POST'])
def create_org(request):
    if request.user.is_authenticated:
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            new_org = serializer.save()
            payload = {
                "status": "success",
                "message": "Organisation Created Successfully",
                "data": {
                    "orgId": new_org.orgId,
                    "name": new_org.name,
                    "description": new_org.description,
                }
            }
            return Response(payload, status=status.HTTP_201_CREATED)
        payload = {
            "status": "Bad Request",
            "message": "Client error",
            "status code": 400,
            "error": serializer.errors
            }
        return Response(payload, status=status.HTTP_400_BAD_REQUEST)
    output = {
        'status': 'Forbidden',
        'message': 'You are not Authenticated',
        'statusCode': 403
        }
    return Response(output, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
def add_users(request, orgId):
    if request.user.is_authenticated:
       serializer = AddUserSerializer(data=request.data, context={'request': request})
       if serializer.is_valid():
          new_user = serializer.validated_data['user']
          org = Organisation.objects.get(orgId=orgId)
          org.members.add(new_user)

          payload = {
              "status": 'success',
              "message": "User added to Organisation Successfully"
          }
          return Response(payload, status=status.HTTP_200_OK)
       return Response(serializer.errors)

    output = {
        'status': 'Forbidden',
        'message': 'You are not Authenticated',
        'statusCode': 403
        }
    return Response(output, status=status.HTTP_403_FORBIDDEN)

# from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Organisation, User
# from django.contrib.auth import authenticate, get_user_model

# Profile = get_user_model()


# # Rest Framework
# from .serializers import UserSerializer, OrganisationSerializer
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework.parsers import JSONParser
# from rest_framework import status
# from rest_framework.authtoken.models import Token


def index(request):
    context = {
        "hello": "hello"
    }
    return JsonResponse(context, safe=False)


# @api_view(['POST'])
# def register(request):
#     if request.method == 'POST':
#         new_user = UserSerializer(data=request.data)
#         if new_user.is_valid():
#             # save new user
#             new_user.save()

#             # create organisation
#             # org_name = f"{str(new_user.firstName)}'s Organisation"
#             # new_org = Organisation.objects.create(name=org_name,members=new_user)
#             # new_org.save()

#             return Response(new_user.data, status=status.HTTP_201_CREATED)
        
#         return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)
    


# @api_view(['POST'])
# def login_user(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('email')

#         user = authenticate(username=email, password=password)

#         if user != None:
#             token, _ = Token.objects.get_or_create(user=user)
            
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
        
#         return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user': {
                    'userId': user.userId,
                    'email': user.email,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

User = get_user_model()


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email is None or password is None:
        return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, email=email, password=password)

    if user is not None:
        tokens = get_tokens_for_user(user)
        return Response({
            'refresh': tokens['refresh'],
            'access': tokens['access'],
            'user': {
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName
            }
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def get_users(request):
    user = User.objects.all()
    serializer = UserSerializer(data=user, many=True)
    return JsonResponse(serializer, safe=False)
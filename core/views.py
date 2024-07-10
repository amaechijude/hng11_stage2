from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.http.response import JsonResponse

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
            
            #tokens
            tokens = get_tokens_for_user(user)
            user_data = {
                    "status": status.HTTP_201_CREATED,
                    "message": "Registration Successful",
                    
                    "data": {
                        #'refresh': tokens['refresh'],
                        'access': tokens['access'],

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

        
        
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('email')

        if len(str(email)) < 1 or len(str(password)) < 1:
            output = {"error": "Provide email and password"}
            return Response(output, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request,email=email, password=password)



        if user is not None:
            #token, _ = Token.objects.get_or_create(user=user)

            user_data = {
             #   'refresh': tokens['refresh'],
              #  'access': tokens['access'],
              "message": "Login Successful",
                'user': {
                    'userId': user.userId,
                    'email': user.email,
                    'firstName': user.firstName,
                    'lastName': user.lastName,
                    'phone': user.phone,
                }
            }
            return Response(user_data, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


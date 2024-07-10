import json
import logging

from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
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
                            },

                        "organisation": {
                            "OrgId": user_org.orgId,
                            "org name": user_org.name,
                        }
                        }
                    }
            return Response(user_data, status=status.HTTP_201_CREATED)

        
        
        return Response(new_user.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({
            # 'refresh': tokens['refresh'],
            'access': tokens['access'],
            'user': {
                'email': user.email,
                'firstName': user.firstName,
                'lastName': user.lastName
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#class login_user(APIView):
#    def post(self, request):
#        try:
#           data = json.loads(request.body)
#           login_user = authenticate(username=data.get("email"), password=data.get("password"))
#           if login_user is not None:
#               context = {"message": f"User {login_user.email} successfully logged in"}
 
 #return Response(context, status.HTTP_202_ACCEPTED)
  #          else:
   #             return Response({"message": "Invalid Credentials"}, status.HTTP_401_UNAUTHORIZED)
    #    except Exception as e:
     #       logging.exception(e)
      #      return Response({"message": "Error occurred"}, status.HTTP_400_BAD_REQUEST)

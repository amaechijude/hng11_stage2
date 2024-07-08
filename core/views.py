from django.shortcuts import render
from django.http.response import JsonResponse
# from django.contrib.auth.models import get_user_model
from .models import User, Organisation
# from django.contrib.auth.decorators import

# Rest Framework
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

# Create your views here.


# User = get_user_model()

def index(request):
    context = {
        "hello": "hello"
    }
    return JsonResponse(context, safe=False)


@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        new_user = UserSerializer(data=request.data)
        if new_user.is_valid():
            # save new user
            new_user.save()

            # create organisation
            org_name = f"{str(new_user.firstName)}'s Organisation"
            new_org = Organisation.objects.create(name=org_name,members=new_user)


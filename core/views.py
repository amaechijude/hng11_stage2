from django.shortcuts import render

from .serializers import *
from .models import *
from rest_framework.parsers import JSONParser

from django.contrib.auth.models import get_user_model

from django.contrib.auth.decorators import csrf_exempt
# Create your views here.


User = get_user_model()

def index(request):
    pass


@csrf_exempt
def register(request):
    if request.method == 'POST':
        user = 

from rest_framework import serializers
from .models import *

class UserSerializer(serializers):
    class Meta:
        model = User
        fields = '__all__'


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'



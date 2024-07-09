from rest_framework import serializers
from .models import Organisation, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email','password', 'phone']
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            #userId = validated_data['userId'],
            firstName = validated_data['firstName'],
            lastName = validated_data['lastName'],
            email = validated_data['email'],
            password = (validated_data['password']),
            phone = validated_data['phone']
        )
        user.save()
        return user


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


# from django.contrib.auth.models import User
# from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             email=validated_data['email'],
#             password=validated_data['password'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name']
#         )
#         return user

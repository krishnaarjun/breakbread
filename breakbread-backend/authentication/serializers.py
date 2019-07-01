from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value: str):
        return make_password(value)

    class Meta:
        model = User
        fields = ('id', 'last_login', 'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
                  'first_name', 'last_name', 'password')


from rest_framework import serializers
from.models import User
 
 
class UserAuthSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name','date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}

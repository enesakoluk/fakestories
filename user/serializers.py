from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from user.models import Profile,UserFollowing
from django.contrib.auth.models import User
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']    
        )    
        user.set_password(validated_data['password'])
        user.save()
        return user



class ProfileSerializer(serializers.ModelSerializer):
    # profile_relate  =UserSerializer()
    class Meta:
        model = Profile
        fields = [ "id","user", 'bio',"website","visible","premium"]

class UserSerializer(serializers.ModelSerializer):
   
    profile_relate = ProfileSerializer()
    class Meta:
        model = User
        fields = [ "id",'username', 'email', 'first_name', 'last_name',"profile_relate"]

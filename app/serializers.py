from rest_framework import serializers
from app.models import PostModel ,CategoryModel
from django.contrib.auth.models import User
from user.serializers import UserSerializer


class categorySerializer(serializers.ModelSerializer):
    class Meta:
             model=CategoryModel
             fields=("id","title","stream","created_at")


class postSerializer(serializers.ModelSerializer):
    # user_related=serializers.ReadOnlyField()
    favori=UserSerializer(many=True, read_only=True)
    like=UserSerializer(many=True, read_only=True)
    user=UserSerializer( read_only=True)
    category=categorySerializer(many=True, read_only=True)
    
    class Meta:
             model=PostModel
             fields=("id","user","isVideo","link","stream","title","like","category","favori","created_at")


class categorygetSerializer(serializers.ModelSerializer):
    category_related=postSerializer(many=True, read_only=True)
    class Meta:
             model=CategoryModel
             fields=("id","title","stream","created_at","category_related")

from rest_framework import serializers
from app.models import PostModel ,CategoryModel,ReportModel
from django.contrib.auth.models import User
from user.serializers import UserSerializer,FollowUserSerializer
class categorySerializer(serializers.ModelSerializer):
    class Meta:
             model=CategoryModel
             fields=("id","title","stream","language","created_at")
class postSerializer(serializers.ModelSerializer):
    # user_related=serializers.ReadOnlyField()
    favori=FollowUserSerializer(many=True, read_only=True)
    like=FollowUserSerializer(many=True, read_only=True)
    user=FollowUserSerializer( read_only=True)
    category=categorySerializer(many=True, read_only=True)
    
    class Meta:
             model=PostModel
             fields=("id","user","isVideo","link","language","description","stream","title","like","category","favori","created_at")

class categorygetSerializer(serializers.ModelSerializer):
    category_related=postSerializer(many=True, read_only=True)
    class Meta:
             model=CategoryModel
             fields=("id","title","stream","language","created_at","category_related")
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
             model=ReportModel
             fields=("id","user","reportuser","language","comment")

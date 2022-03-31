from rest_framework import serializers
from app.models import PostModel
from django.contrib.auth.models import User
class postSerializer(serializers.ModelSerializer):
    user_related=serializers.RelatedField(source='user.username', read_only=True)
    class Meta:
             model=PostModel
             fields=("id","user","isVideo","link","stream","title","like","category","favori","created_at","user_related")



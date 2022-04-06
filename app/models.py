
from django.db import models
from user.serializers import UserSerializer
from rest_framework import serializers
import json
# Create your models here.
from django.contrib.auth.models import User
class CategoryModel(models.Model):
    title= models.TextField(max_length=200, blank=True,null=True)
    stream=models.IntegerField(default=0,db_index=True)
    language=models.TextField(max_length=200, blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True,db_index=True)


class PostModel(models.Model):
    user =  models.ForeignKey(User,related_name="post_related",on_delete=models.CASCADE)
    isVideo=models.BooleanField(db_index=True)
    link=models.URLField(max_length=200, blank=True)
    stream=models.IntegerField(default=0,db_index=True)
    title= models.TextField(max_length=400, blank=True,null=True)
    language=models.TextField(max_length=200, blank=True,null=True)
    like = models.ManyToManyField(User, blank=True, related_name="like_related",db_index=True)
    category =models.ManyToManyField(CategoryModel,related_name="category_related")
    favori = models.ManyToManyField(User, blank=True, related_name="favori_related")
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True,db_index=True)
    class Meta:
        ordering = ('-created_at',)
   
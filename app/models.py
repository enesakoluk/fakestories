
from django.db import models
from user.serializers import UserSerializer
from rest_framework import serializers
import json
# Create your models here.
from django.contrib.auth.models import User
class CategoryModel(models.Model):
    title= models.TextField(max_length=200, blank=True)
    stream=models.IntegerField(default=0,db_index=True)
    language=models.TextField(default="en_EN",max_length=200, blank=True)
    # ----
    isVideo=models.BooleanField(db_index=True)
    imagelink=models.URLField(default="https://i.pinimg.com/564x/16/93/d2/1693d2df0f81fbeb9095e99d33c3c3fd.jpg",max_length=600, blank=True)
    # ----
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True,db_index=True)
    # BURADAN EMİN DEĞİLİM HATA CIKARSA KAPACAM
    def __str__(self):
        return  self.title

class PostModel(models.Model):
    user =  models.ForeignKey(User,related_name="post_related",on_delete=models.CASCADE)
    isVideo=models.BooleanField(db_index=True)
    link=models.URLField(max_length=600, blank=True)
    stream=models.IntegerField(default=0,db_index=True)
    title= models.TextField(default="",max_length=400, blank=True)
    description= models.TextField(default="",max_length=2000, blank=True)
    language=models.TextField(default="en_EN",max_length=200, blank=True)
    like = models.ManyToManyField(User, blank=True, related_name="like_related",db_index=True)
    category =models.ManyToManyField(CategoryModel,blank=True,related_name="category_related")
    favori = models.ManyToManyField(User, blank=True, related_name="favori_related")
    
    created_at = models.DateTimeField(auto_now_add=True,blank=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,db_index=True)
    class Meta:
        ordering = ('-created_at',)

class ReportModel(models.Model):
    user =  models.ForeignKey(User,related_name="report_related",on_delete=models.CASCADE)
    reportuser=models.ForeignKey(User,related_name="reportuser_related",on_delete=models.CASCADE)
    comment=models.TextField(default="",max_length=400, blank=True,null=True)
    language=models.TextField(default="en_EN",max_length=200, blank=True,null=True)
    isactive=models.BooleanField(db_index=True,default=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True,db_index=True)
    class Meta:
        ordering = ('-created_at',)
   
   
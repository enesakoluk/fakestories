
import json
from django.shortcuts import render

from rest_framework.generics import RetrieveDestroyAPIView,ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework import pagination 
from rest_framework import filters
from rest_framework.views import APIView
from app.models import CategoryModel,PostModel
from app.serializers import postSerializer ,categorygetSerializer,categorySerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from app.filter import PostFilter,categoriFilter
from django_filters.rest_framework import DjangoFilterBackend
from user.models import UserFollowing


#----CDN
import requests
import uuid
from BunnyCDN.Storage import Storage 
obj_storage = Storage("3c3d09ce-37d1-4978-bccc4fe97f00-5516-40dd","mystories")
zone="https://uygunsuzad.b-cdn.net/"
#----CDN
#ftp password + store isimi

from django.http import Http404

class postlistCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = postSerializer
    queryset = PostModel.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title',"user__username","category__title"]
    filterset_class = PostFilter
    def perform_create(self, serializer):
        incoming_data = self.request.data["file"].open()
        myuuid = uuid.uuid4()
        contenttype=str(self.request.data["file"]).split(".")[-1]
        filename=str(myuuid)+"."+contenttype
        response = requests.put(obj_storage.base_url+filename, data=incoming_data, headers=obj_storage.headers)
        if(response.status_code==201):
            serializer.save(user=self.request.user ,link=zone+filename )
            
#takip edilenlerin postları           
class FolowPostViews(APIView):
    def get(self, request, format=None):
        try:
            followed_people = UserFollowing.objects.filter(user_id=request.user).values('following_user_id')
            stories = PostModel.objects.filter(user__in=followed_people) 
            serializer = postSerializer(stories,many=True)
            return Response(serializer.data)
        except PostModel.DoesNotExist:
            raise Http404    


#creat ozelleşecek
class postGetView(RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = postSerializer
    queryset = PostModel.objects.all()

    def get(self, request,pk, *args, **kwargs):
        
        try:
            post = PostModel.objects.get(pk=pk)
            post.stream += 1
            post.save()
               
            return self.retrieve(request, *args, **kwargs)
            
            # return HttpResponse(snippet.following.count())
            
        except PostModel.DoesNotExist:
            raise Http404
        

    def delete(self, request,pk, *args, **kwargs):
        
        try:
            post = PostModel.objects.get(pk=pk)
            if request.user.id==post.user.id:
               
                return self.destroy(request, *args, **kwargs)
            else:
                return Response(status=404)
            # return HttpResponse(snippet.following.count())
            
        except PostModel.DoesNotExist:
            raise Http404
      


#Category
class CategoryGetView(RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = categorygetSerializer
    queryset = CategoryModel.objects.all()

    def get(self, request,pk, *args, **kwargs):
        try:
            post = CategoryModel.objects.get(pk=pk)
            post.stream += 1
            post.save()
               
            return self.retrieve(request, *args, **kwargs)
            
            # return HttpResponse(snippet.following.count())
            
        except CategoryModel.DoesNotExist:
            raise Http404
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        #buraya sahiplik koyulacak
        return self.destroy(request, *args, **kwargs)


class categoryCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = categorySerializer
    queryset = CategoryModel.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter,DjangoFilterBackend]
    search_fields = ['title',"language"]
    filterset_class = categoriFilter


#like
class likeViews(APIView):
    
    def get(self, request,pk, format=None):
        try:
            post = PostModel.objects.get(pk=pk)
            # user = User.objects.get(pk=self.request.user.id)
            if request.user in post.like.all():
                post.like.remove(request.user )
                #unlike
            else:
                post.like.add(request.user)

                #like
            
            serializer = postSerializer(post)
            return Response(serializer.data)
            # return HttpResponse(snippet.following.count())
            
        except PostModel.DoesNotExist:
            raise Http404

class favoriteViews(APIView):
    
    def get(self, request,pk, format=None):
        try:
            post = PostModel.objects.get(pk=pk)
            # user = User.objects.get(pk=self.request.user.id)
            if request.user in post.favori.all():
                post.favori.remove(request.user )
                print("silindi")
                #unlike
            else:
                post.favori.add(request.user)
                print("eklendi")
                #like
            
            serializer = postSerializer(post)
            return Response(serializer.data)
            # return HttpResponse(snippet.following.count())
            
        except PostModel.DoesNotExist:
            raise Http404
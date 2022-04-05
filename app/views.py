
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
from app.filter import PostFilter
#django.core.files.uploadedfile.InMemoryUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from publitio import PublitioAPI
publitio_api = PublitioAPI(key='l3oH2rmMetJp5tpVqgGj', secret='lA00WcRcxfh9otHy0t3mJwv03g7t7t4G')
#----
from BunnyCDN.Storage import Storage 
from BunnyCDN.CDN import CDN
import requests
import uuid

obj_storage = Storage("3c3d09ce-37d1-4978-bccc4fe97f00-5516-40dd","mystories")
zone="https://uygunsuzad.b-cdn.net/"
#ftp password + store isimi
print(obj_storage.GetStoragedObjectsList("."))
#----
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
           
            
       
        
    # def get(self, request, *args, **kwargs):

    #     return self.list(request, *args, **kwargs)
    


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
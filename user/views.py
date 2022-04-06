from django.shortcuts import render
# from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView,CreateAPIView
from rest_framework.permissions import DjangoModelPermissions 
from rest_framework.response import Response
from django.contrib.auth.models import User
from user.models import Profile,UserFollowing
from user.serializers import ProfileSerializer,UserSerializer
from django.http import HttpResponse
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend
from publitio import PublitioAPI
publitio_api = PublitioAPI(key='l3oH2rmMetJp5tpVqgGj', secret='lA00WcRcxfh9otHy0t3mJwv03g7t7t4G')
#----CDN
import requests
import uuid
from BunnyCDN.Storage import Storage 
obj_storage = Storage("3c3d09ce-37d1-4978-bccc4fe97f00-5516-40dd","mystories")
zone="https://uygunsuzad.b-cdn.net/"
#----CDN

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ProfileViewUpdateDestroyAPIView(APIView):

    def get_object(self):
        try:
            return Profile.objects.get(user=self.request.user.id)
        except Profile.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        try:
            snippet = User.objects.get(pk=self.request.user.id)
            serializer = UserSerializer(snippet)
            return Response(serializer.data)
            
        except Profile.DoesNotExist:
            raise Http404
        
    def put(self, request, format=None):
       
        profile= Profile.objects.get(pk=self.request.user.id)
        incoming_data = self.request.data["file"].open()
        myuuid = uuid.uuid4()
        contenttype=str(self.request.data["file"]).split(".")[-1]
        filename=str(myuuid)+"."+contenttype
        response = requests.put(obj_storage.base_url+filename, data=incoming_data, headers=obj_storage.headers)
        if(response.status_code==201):
            serializer = ProfileSerializer(profile, data={"profileimage":zone+filename} ,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, format=None):
        snippet = self.get_object()
        serializer = ProfileSerializer(snippet, data=request.data ,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class followViews(APIView):
    

    def get(self, request,pk, format=None):
        try:
            usertofollow = User.objects.get(pk=pk)
            snippet = User.objects.get(pk=self.request.user.id)
            
            if UserFollowing.objects.filter(following_user_id=usertofollow, user_id=request.user).exists():
                UserFollowing.objects.filter(following_user_id=usertofollow, user_id=request.user).delete()
            else:
                m = UserFollowing(following_user_id=usertofollow, user_id=request.user)  # creating like object
                m.save()  # saves into database
            print(snippet.following)
            serializer = UserSerializer(usertofollow)
            return Response(serializer.data)
            # return HttpResponse(snippet.following.count())
            
        except Profile.DoesNotExist:
            raise Http404
        
 


class profileView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer   
    queryset = User.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['username']
    

class profileGetView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


#block
class blockViews(APIView):
    
    def get(self, request,pk, format=None):
        try:
            blockpost = User.objects.get(pk=pk)
            post = Profile.objects.get(pk=self.request.user.id)
            if blockpost in post.block.all():
                post.block.remove(blockpost )
                #unlike
            else:
                post.block.add(blockpost)

                #like
            
            serializer = ProfileSerializer(post)
            return Response(serializer.data)
            # return HttpResponse(snippet.following.count())
            
        except Profile.DoesNotExist:
            raise Http404
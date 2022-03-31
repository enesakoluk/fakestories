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
from user.models import Profile
from user.serializers import ProfileSerializer,UserSerializer


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
        snippet = self.get_object()
        serializer = ProfileSerializer(snippet, data=request.data)
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

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
#django.core.files.uploadedfile.InMemoryUploadedFile
from django.core.files.uploadedfile import InMemoryUploadedFile

# Create your views here.
from publitio import PublitioAPI
publitio_api = PublitioAPI(key='l3oH2rmMetJp5tpVqgGj', secret='lA00WcRcxfh9otHy0t3mJwv03g7t7t4G')
from django.http import Http404
class postlistCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = postSerializer
    queryset = PostModel.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['title']
    def perform_create(self, serializer):
        incoming_data = self.request.data["file"].open()
        test= publitio_api.create_file(file=incoming_data,
            title='My title',
            description='My description')
        print(test["url_short"])
        serializer.save(user=self.request.user ,link=test["url_short"] )
    def get(self, request, *args, **kwargs):

        return self.list(request, *args, **kwargs)
    


#creat ozelleşecek
class postGetView(RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = postSerializer
    queryset = PostModel.objects.all()

    def get(self, request,pk, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request,pk, *args, **kwargs):
        #buraya sahiplik koyulacak
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

    def get(self, request, *args, **kwargs):
        
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
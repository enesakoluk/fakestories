from django.shortcuts import render

from rest_framework.generics import RetrieveDestroyAPIView,ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework import pagination 
from rest_framework import filters

from app.models import CategoryModel,PostModel
from app.serializers import postSerializer ,categorygetSerializer,categorySerializer

# Create your views here.
class postlistCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = postSerializer
    queryset = PostModel.objects.all()
    filter_backends = [filters.OrderingFilter,filters.SearchFilter]
    search_fields = ['title']


#creat ozelleşecek
class postGetView(RetrieveDestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = postSerializer
    queryset = PostModel.objects.all()

    def get(self, request, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        #buraya sahiplik koyulacak
        return self.destroy(request, *args, **kwargs)


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
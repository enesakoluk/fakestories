
import json
from django.shortcuts import render

from rest_framework.generics import RetrieveDestroyAPIView,ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework import pagination
from rest_framework import filters
from rest_framework.views import APIView
from app.models import CategoryModel,PostModel,ReportModel
from app.serializers import ReportSerializer, postSerializer ,categorygetSerializer,categorySerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from app.filter import PostFilter,categoriFilter
from django_filters.rest_framework import DjangoFilterBackend
from user.models import UserFollowing
from user.models import Profile
from rest_framework import status
#----CDN
import requests
import uuid
from BunnyCDN.Storage import Storage
obj_storage = Storage("51106d1f-cd35-4a01-b9495fa782f6-230d-4c00","mystories22")
zone="https://mysitesname.b-cdn.net//"
# obj_storage = Storage("3c3d09ce-37d1-4978-bccc4fe97f00-5516-40dd","mystories")
# zone="https://uygunsuzad.b-cdn.net/"
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
           
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
# ---costum
    
        if 'categorys' in self.request.data:
            user = Profile.objects.get(pk=self.request.user.id)
            post = PostModel.objects.get(pk=serializer.data["id"])
            categorylisttitle=json.loads(self.request.data["categorys"])
            print(categorylisttitle)
            for getitle in categorylisttitle:
                print(getitle)
                categoryfil=CategoryModel.objects.filter(title=getitle)
                print(categoryfil.count())
                if(categoryfil.count() !=0):
                    model=categoryfil.first()
                    post.category.add(model)
                else:
                    serializerr = CategoryModel(language=user.language,title=getitle)
                    serializerr.save()
                    model=serializerr
                    post.category.add(model)
# ---costum
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#takip edilenlerin postlar??
class FolowPostViews(APIView):
    def get(self, request, format=None):
        try:
            if 'isVideo' in self.request.query_params:
                value=self.request.query_params["isVideo"]
                followed_people = UserFollowing.objects.filter(user_id=request.user).values('following_user_id')
                stories = PostModel.objects.filter(user__in=followed_people,isVideo=value.capitalize())
                serializer = postSerializer(stories,many=True)

            else:
                print("---------")
                followed_people = UserFollowing.objects.filter(user_id=request.user).values('following_user_id')
                stories = PostModel.objects.filter(user__in=followed_people)
                serializer = postSerializer(stories,many=True)
            return Response(serializer.data)
        except PostModel.DoesNotExist:
            raise Http404


#creat ozelle??ecek
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
                linkurl=post.link.split("/")[-1]
                print(post.link.split("/")[-1])
                response = requests.delete(obj_storage.base_url+linkurl, headers=obj_storage.headers)
                if(response.status_code==200):
                    print("silindi post cdn")
                else:
                    print("post cdn silinemedi")
            #    TODO: burada cdn silinecek
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
            # if 'isVideo' in self.request.query_params:
            #     value=self.request.query_params["isVideo"]
            #     print(value)
            #     test=PostModel.objects.filter(category=post,isVideo=value)
            #     print(test)
            # else:
            #     print("asd")

            # post = CategoryModel.objects.get(pk=pk)
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
    search_fields = ['title',"language","isVideo"]
    filterset_class = categoriFilter

class PostAddCategoryViews(APIView):
    def post(self, request,pk, format=None):
        try:
            user = Profile.objects.get(pk=request.user.id)
            post = PostModel.objects.get(pk=pk)
            if 'category' in self.request.data:
                categorylisttitle=self.request.data["category"]
                for getitle in categorylisttitle:
                    categoryfil=CategoryModel.objects.filter(title=getitle)
                    print(categoryfil.count())
                    if(categoryfil.count() !=0):
                        model=categoryfil.first()
                        if model in post.category.all():
                            post.category.remove(model)
                        else:
                            post.category.add(model)
                    else:
                        serializer = CategoryModel(language=user.language,title=getitle)
                        serializer.save()
                        model=serializer
                        if model in post.category.all():
                            post.category.remove(model)
                        else:
                            post.category.add(model)




                return Response(data={"status":"201","report":"ok"},status=201)


            else:
                return Response(data={"status":"404","report":"test"},status=404)
        except User.DoesNotExist:
            raise Http404

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

#report
class ReportViews(APIView):

    def post(self, request,pk, format=None):
        try:
            if 'comment' in self.request.data:
                if 'language' in self.request.data:
                    reportuser_ = User.objects.get(pk=pk)
                    user_ = User.objects.get(pk=self.request.user.id)
                    serializer = ReportModel(user=user_,reportuser=reportuser_,comment=self.request.data["comment"],language=self.request.data["language"])
                    serializer.save()  #
                    return Response(data={"status":"201","report":"ok"},status=201)
                else:
                    return Response(data={"status":"404","report":"language is empty"},status=404)

            else:
                return Response(data={"status":"404","report":"comment is empty"},status=404)
        except User.DoesNotExist:
            raise Http404
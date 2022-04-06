from django.urls import path
from user.views import  RegisterView
from rest_framework_simplejwt import views as jwt_views
from user.views import ProfileViewUpdateDestroyAPIView
from app.views import postlistCreateView,postGetView,CategoryGetView,categoryCreateView,likeViews,favoriteViews,FolowPostViews



urlpatterns = [
    
    path('post/', postlistCreateView.as_view()),
    path('post/<int:pk>', postGetView.as_view()),
    path('category/<int:pk>', CategoryGetView.as_view()),
    path('category/', categoryCreateView.as_view()),
    path('like/<int:pk>', likeViews.as_view()),
    path('favorite/<int:pk>', favoriteViews.as_view()),
    path('followingpost/', FolowPostViews.as_view()),
   
          ]
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile_relate",on_delete=models.CASCADE)
    following = models.ManyToManyField(User, blank=True, related_name="followers", symmetrical=False)
    bio = models.TextField(max_length=200, blank=True, default="Bio")
    website = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)
    # def __str__(self):
    #     return self.user
    def __str__(self):
          return f"{self.user.username} Profile"




    
    
    


    
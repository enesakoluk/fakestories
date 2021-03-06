
from django.db import models
from django.contrib.auth.models import User
class Profile(models.Model):
    user = models.OneToOneField(User,related_name="profile_relate",on_delete=models.CASCADE,db_index=True)
    #following = models.ManyToManyField(User, blank=True, related_name="followers", symmetrical=False)
    bio = models.TextField(default="",max_length=200, blank=True)
    premium=models.BooleanField(default=False)

    download=models.IntegerField(default=0,db_index=True)
    language=models.TextField(default="en_EN",max_length=200, blank=True,null=True)
#----
    profileimage=models.URLField(default="https://i.pinimg.com/564x/c9/e3/e8/c9e3e810a8066b885ca4e882460785fa.jpg",max_length=200, blank=True)
    block = models.ManyToManyField(User,related_name="block_relate",db_index=True,blank=True)
#----
    website = models.URLField(max_length=200, blank=True)
    visible=models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True,db_index=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True,db_index=True)
    def username(self):
        return self.user.username
    def __str__(self):
          return f"{self.user.username}"


class UserFollowing(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE ,related_name="following",db_index=True)
    following_user_id = models.ForeignKey(User,on_delete=models.CASCADE, related_name="followers",db_index=True)
    confirmed=models.BooleanField(default=True,db_index=True)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)
    def save(self, *args, **kwargs):
        super(UserFollowing, self).save(*args, **kwargs)
        
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id','following_user_id'],  name="unique_followers")
        ]
        ordering = ["-created_at"]
    # def __str__(self):
    #     f"{self.user_id} follows {self.following_user_id}"
    
    
    


    
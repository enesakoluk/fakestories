from django.contrib import admin
from user.models import Profile
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( 'id','user',"count_followers","count_following","following_list","followers_list")

admin.site.register(Profile,ProfileAdmin)


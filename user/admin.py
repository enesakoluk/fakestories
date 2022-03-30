from django.contrib import admin
from user.models import Profile,UserFollowing
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( 'id','user')

admin.site.register(Profile,ProfileAdmin)

class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ( 'id','user_id',"following_user_id","confirmed","created_at")

admin.site.register(UserFollowing,UserFollowingAdmin)


from django.contrib import admin
from user.models import Profile,UserFollowing
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ( 'id','user',"username","bio","language","profileimage","premium")
    search_fields =  ('user__username', )
    list_filter = ('language', 'premium')
    
    # ordering = ('language',)

admin.site.register(Profile,ProfileAdmin)

class UserFollowingAdmin(admin.ModelAdmin):
    list_display = ( 'id','user_id',"following_user_id","confirmed","created_at")

admin.site.register(UserFollowing,UserFollowingAdmin)


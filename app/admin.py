from django.contrib import admin

from django.contrib import admin
from app.models import PostModel,CategoryModel,ReportModel
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ( 'id',"user",'title',"language","link","isVideo","created_at")
    search_fields =  ('user__username',"title" )
    list_filter = ('language', 'isVideo')

admin.site.register(PostModel,PostAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','title',"language","created_at")
    search_fields =  ('language',"title" )
    list_filter = ('language',)

admin.site.register(CategoryModel,CategoryAdmin)


class ReportModelAdmin(admin.ModelAdmin):
    list_display = ( 'id','user',"reportuser","comment","language","isactive","created_at")

admin.site.register(ReportModel,ReportModelAdmin)


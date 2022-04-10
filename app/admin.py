from django.contrib import admin

from django.contrib import admin
from app.models import PostModel,CategoryModel,ReportModel
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ( 'id',"user",'title',"language","link","isVideo","created_at")
    

admin.site.register(PostModel,PostAdmin)



class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','title',"language","created_at")

admin.site.register(CategoryModel,CategoryAdmin)


class ReportModelAdmin(admin.ModelAdmin):
    list_display = ( 'id','user',"reportuser","comment","language","isactive","created_at")

admin.site.register(ReportModel,ReportModelAdmin)


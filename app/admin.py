from django.contrib import admin

from django.contrib import admin
from app.models import PostModel,CategoryModel
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ( 'id','title')

admin.site.register(PostModel,PostAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'id','title')

admin.site.register(CategoryModel,CategoryAdmin)


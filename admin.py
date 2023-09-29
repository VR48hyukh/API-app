from django.contrib import admin
from .import models
from .models import (UserModel,Product,LessonModel,Access,ViewsModel,LessonProductModel)


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'owner']

@admin.register(LessonModel)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'link', 'duration']

@admin.register(Access)
class AccessModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'value']

@admin.register(ViewsModel)
class ViewsModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'duration']

@admin.register(LessonProductModel)
class LessonProductModelAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'product']
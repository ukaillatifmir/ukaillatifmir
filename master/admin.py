from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(user)
class AdminLogin(admin.ModelAdmin):
    list_display=('Email','password','user_name','last_name','Gender',)
@admin.register(business_card)
class AdminBusiness(admin.ModelAdmin):
    list_display=('email','name','phone',)

@admin.register(cover)
class admin_image(admin.ModelAdmin):
    list_display=('email','images','discription',)
@admin.register(post)
class admin_image(admin.ModelAdmin):
    list_display=('link','all_images',)
from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('',Home.as_view(),name='Home'),
    path('index',Index.as_view(),name='index'),
    path('inner/dash',dash.as_view(),name='dash'),
    path('registeration',Index.as_view(),name='index'),
    path('login',login.as_view(),name='login'),
    path('inner/logout',logout.as_view(),name='innerlogout'),
    path('inner/<my_id>',inner.as_view(),name='inner'),
    path('homeinner/<my_id>',homeinner.as_view(),name='homeinner'),
    path('dash',dash.as_view(),name='dash'),
    
    path('logout',logout.as_view(),name='logout'),
    
    path('card',businesscard.as_view(),name='mail'),
    path('imagepost',imagepost.as_view(),name='imagepost'),
    

    
    
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
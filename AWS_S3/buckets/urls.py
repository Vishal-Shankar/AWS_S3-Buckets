from django.contrib import admin
from django.urls import path,include
from buckets import views

app_name='buckets'


urlpatterns = [
path('',views.home,name='home'),
path('login/',views.login,name='login'),
path('create/',views.create,name='create'),
path('delete/',views.delete,name='delete'),
path('copy/',views.copy,name='copy'),
path('move/',views.move,name='move'),
path('create/<str:fn>/',views.files),
path('login/<str:fn>/',views.files),
path('delete/<str:fn>/',views.files),
path('login/<str:fn>/upld.html',views.upload),
path('create/<str:fn>/upld.html',views.upload),
path('delete/<str:fn>/upld.html',views.upload),
]
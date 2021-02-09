from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('post/<str:post_slug>/', views.post, name='post'),
]

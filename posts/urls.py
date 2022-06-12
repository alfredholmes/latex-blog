from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('post/<str:post_slug>/', views.post, name='post'),
	path('post/<str:post_slug>/<str:html_slug>', views.post_page, name='post_page'),
	path('post/collections>', views.collections, name='collections'),
	path('post/collections/<str:collection_slug>', views.collection, name='collection'),
	path('post/about', views.about, name='about'),
]

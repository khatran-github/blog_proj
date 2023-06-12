from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('topics/', views.topics, name='topics'),
    path('topics/<slug:slug>/', views.topic, name='topic'),
    path('<slug:slug>/', views.entry_detail, name='entry_detail'),
    path('@<str:username>/blogs/', views.user_entries, name='user_entries'),
    path('new_blog/<slug:slug>/', views.new_entry, name='new_entry'),
    path('edit_blog/<slug:slug>/', views.edit_entry, name='edit_entry'),
    path('delete_blog/<slug:slug>/', views.delete_entry, name='delete_entry'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.room_list, name='room_list'),  
    path('chat/<str:room_name>/', views.room, name='chat_room'),  
    path('chat/delete/<str:room_name>/', views.delete_room, name='delete_room'),
    path('chat/private/<str:username>/', views.private_chat, name='private_chat'),
    path('chat/private/', views.private_chat_list, name='private_chat_list'),

]

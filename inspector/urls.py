from django.urls import path

from . import views

urlpatterns = [
    path('khook/', views.handle_plex, name='index'),
    path('notification/posted', views.notification_posted, name='notification_posted'),
    path('notification/removed', views.notification_removed, name='notfication_removed'),
    path('call/started', views.call_started, name='call_started'),
    path('call/ended', views.call_ended, name='call_ended')
]

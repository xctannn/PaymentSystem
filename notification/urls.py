from django.urls import path
from .views import GetNotifications, DeleteNotification
from . import views

urlpatterns = [
    path('', GetNotifications, name = 'notification-home'),
    path('<noti_id>/delete', DeleteNotification, name='notification-delete')
]
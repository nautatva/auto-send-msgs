from django.urls import path
from . import views

urlpatterns = [
    path(r'schedule', views.schedule_event_messages),
    # path(r'get', views.get_scheduled_messages)
]

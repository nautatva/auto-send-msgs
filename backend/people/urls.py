from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.save_birthdays_from_google)
]

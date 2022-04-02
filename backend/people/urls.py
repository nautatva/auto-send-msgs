from django.urls import path
from . import views

urlpatterns = [
    path(r'get_data_from_google', views.get_contacts_from_google),
    path(r'', views.extract_birthdays_from_contacts),
]

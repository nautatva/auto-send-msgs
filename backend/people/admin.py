from django.contrib import admin
from people.models import Contact, Event
from utils.django_utils import AdminWithUserData


# TODO: Show all fields for contact, also add filters
admin.site.register(Contact, AdminWithUserData)
admin.site.register(Event, AdminWithUserData)

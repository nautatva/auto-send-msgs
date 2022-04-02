from django.contrib import admin
from people.models import Contact, Event


# TODO: Show all fields for contact, also add filters
admin.site.register(Contact)
admin.site.register(Event)

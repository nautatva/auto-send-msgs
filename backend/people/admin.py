from django.contrib import admin
from people.models import Contact


# TODO: Show all fields for contact, also add filters
admin.site.register(Contact)

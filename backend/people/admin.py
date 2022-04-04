from django.contrib import admin
from people.models import Contact, Event
from utils.django_utils import BaseAdmin


class ContactAdmin(BaseAdmin):
    readonly_fields = ('source',)


# TODO: Show all fields for contact, also add filters
admin.site.register(Contact, ContactAdmin)
admin.site.register(Event, BaseAdmin)

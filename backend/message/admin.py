from django.contrib import admin
from message.models import ScheduledMessage
from utils.django_utils import BaseAdmin


class ScheduledMessageAdmin(BaseAdmin):
    readonly_fields = ('contact', 'reference_event', 'sent')


admin.site.register(ScheduledMessage, ScheduledMessageAdmin)

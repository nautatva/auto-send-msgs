from django.contrib import admin
from message.models import ScheduledMessage
from utils.django_utils import AdminWithUserData


admin.site.register(ScheduledMessage, AdminWithUserData)

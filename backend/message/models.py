from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# from django.conf import settings
from django.utils import timezone
# from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from django.db.models import Q
from people.models import Contact, Event
from utils.django_utils import BaseModel


class CustomScheduledMessageManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        for obj in objs:
            obj.enrich_details()
        return super().bulk_create(objs, **kwargs)


class ScheduledMessage(BaseModel):
    # objects = BulkUpdateOrCreateQuerySet.as_manager()
    objects = CustomScheduledMessageManager()

    content = models.TextField(blank=False, null=False, default="Hi")  # TextField for custom messages
    time_to_send = models.DateTimeField(blank=False, null=False, default=timezone.now)

    number = PhoneNumberField(blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    reference_event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    reference_event.readonly = True

    sent = models.BooleanField(blank=False, null=False, default=False)
    sent.readonly = True

    def __str__(self):
        return f"{self.number}"

    def enrich_details(self):
        if (self.contact is None) and self.reference_event is not None:
            self.contact = self.reference_event.contact

        if (self.number is None or self.number == '') and self.contact is not None:
            self.number = self.contact.number

    def save(self, *args, **kwargs):
        self.enrich_details()
        super(ScheduledMessage, self).save(*args, **kwargs)

    def bulk_create(self, objs, *args, **kwargs):
        for obj in objs:
            obj.enrich_details()
        super(ScheduledMessage, self).bulk_create(objs, *args, **kwargs)

    class Meta:
        # TODO: Don't allow same msgs to be scheduled
        constraints = [
            models.CheckConstraint(
                check=Q(contact__isnull=False) | Q(number__isnull=False),
                name='not_both_null'
            )
        ]

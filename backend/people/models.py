from django.db import models
from django.conf import settings
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from choices.time import Frequency
from utils.django_utils import BaseModel


class Contact(BaseModel):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    # TODO: Ideal max_length?
    # TODO First name, last name separate?
    name = models.CharField(max_length=150)

    number = PhoneNumberField()

    detail = models.TextField(default=settings.DEFAULT_CONTACT_DETAIL, editable=False)

    source = models.CharField(max_length=25, default=settings.MANUAL_SOURCE, blank=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                'created_by',
                Lower('name'),
                'number',
                name='unique_created_by_name_number',
            ),
        ]


class Event(BaseModel):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # TODO: Make a choice field with other input allowed
    date = models.DateField()
    frequency = models.CharField(choices=Frequency.choices(), max_length=25, default=Frequency.ONCE)

    def __str__(self):
        return f"{self.contact} - {self.name}"

    class Meta:
        constraints = [
            UniqueConstraint(
                'contact',
                Lower('name'),
                'date',
                name='unique_contact_name_date',
            ),
        ]

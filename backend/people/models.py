from django.db import models
from django.conf import settings
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


class Contact(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    # TODO: Ideal max_length?
    # TODO First name, last name separate?
    name = models.CharField(max_length=150)

    number = PhoneNumberField()
    detail = models.TextField(default=settings.DEFAULT_CONTACT_DETAIL)
    source = models.CharField(max_length=25, db_column="source", default=settings.MANUAL_SOURCE)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                'user',
                Lower('name'),
                'number',
                name='unique_user_name_number',
            ),
        ]


class Event(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # TODO: Make a choice field with other input allowed
    date = models.DateField()

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

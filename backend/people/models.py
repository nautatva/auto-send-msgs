from django.db import models
from django.conf import settings
from bulk_update_or_create import BulkUpdateOrCreateQuerySet
from phonenumber_field.modelfields import PhoneNumberField


class Contact(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    number = PhoneNumberField()
    birthday = models.DateField(null=True, blank=True)
    detail = models.TextField(default="Manually filled contact")

    def __str__(self):
        return self.name

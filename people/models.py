from django.db import models
from django.conf import settings
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class Contact(models.Model):
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=50)
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

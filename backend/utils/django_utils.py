from django.contrib import admin
from django.conf import settings
from django.db import models
from django.db.models import Q


class AdminWithUserData(admin.ModelAdmin):
    def get_exclude(self, request, obj=None):
        try:
            hidden_fields = []
            for f in obj._meta.fields:
                try:
                    if f.hidden:
                        hidden_fields.append(f.name)
                except AttributeError:
                    continue
            return hidden_fields
        except Exception:
            # if a new object is to be created the try clause will fail due to missing _meta.fields
            return ""

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ["created_by", "last_modified_by"]
        try:
            for f in obj._meta.fields:
                try:
                    if f.readonly:
                        readonly_fields.append(f.name)
                except AttributeError:
                    continue
            return readonly_fields
        except Exception:
            # if a new object is to be created the try clause will fail due to missing _meta.fields
            return readonly_fields

    # def get_changeform_initial_data(self, request):
    #     data = super(AdminWithUserData, self).get_changeform_initial_data(request)
    #     data['created_by'] = request.user.pk
    #     return data


class BaseModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_created_by",
        editable=False,
        default=1
    )
    last_modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_modified_by",
        editable=False,
        null=True
        # default=1
    )
    # created_by.readonly = True

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=Q(created_by__isnull=False) | Q(last_modified_by__isnull=False),
                name='not_both_null'
            )
        ]

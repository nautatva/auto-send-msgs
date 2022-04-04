from django.contrib import admin
from django.conf import settings
from django.db import models
from django.db.models import Q


class BaseAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # TODO: Filter queryset to allow only self-created objects
        return super(BaseAdmin, self).get_queryset(request)

    def get_exclude(self, request, obj=None):
        custom_hidden_fields = ["created_by", "last_modified_by"]
        hidden_fields = []
        concrete_class_hidden_fields = super(BaseAdmin, self).get_exclude(request, obj)
        if concrete_class_hidden_fields is None:
            return custom_hidden_fields

        for field in concrete_class_hidden_fields:
            hidden_fields.append(field)

        for field in custom_hidden_fields:
            hidden_fields.append(field)

        return hidden_fields

    def get_readonly_fields(self, request, obj=None):
        custom_readonly_fields = ["created_by", "last_modified_by"]
        readonly_fields = []
        concrete_class_readonly_fields = super(BaseAdmin, self).get_readonly_fields(request, obj)
        if concrete_class_readonly_fields is None:
            return custom_readonly_fields

        for field in concrete_class_readonly_fields:
            readonly_fields.append(field)

        for field in custom_readonly_fields:
            readonly_fields.append(field)

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
    )

    class Meta:
        abstract = True
        constraints = [
            models.CheckConstraint(
                check=Q(created_by__isnull=False) | Q(last_modified_by__isnull=False),
                name='not_both_null'
            )
        ]

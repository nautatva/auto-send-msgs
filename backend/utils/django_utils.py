from django.contrib import admin
from django.conf import settings
from django.db import models
from django.db.models import Q
from utils.common_utils import merge_iterables


class BaseAdmin(admin.ModelAdmin):
    # TODO: Permission control to take in account if user is super-user
    def get_queryset(self, request):
        return super(BaseAdmin, self).get_queryset(request).filter(created_by=request.user)

    def get_exclude(self, request, obj=None):
        custom_hidden_fields = ["created_by", "last_modified_by"]
        concrete_class_hidden_fields = super(BaseAdmin, self).get_exclude(request, obj)
        return merge_iterables(concrete_class_hidden_fields, custom_hidden_fields)

    def get_readonly_fields(self, request, obj=None):
        custom_readonly_fields = ["created_by", "last_modified_by"]
        concrete_class_readonly_fields = super(BaseAdmin, self).get_readonly_fields(request, obj)
        return merge_iterables(concrete_class_readonly_fields, custom_readonly_fields)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        """
            Filter the selections to created_by the user
        """
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        field.queryset = field.queryset.filter(created_by=request.user)
        return field

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

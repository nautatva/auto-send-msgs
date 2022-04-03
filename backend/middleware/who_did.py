"""Add user created_by and modified_by foreign key refs to any model automatically.
   Almost entirely taken from https://github.com/Atomidata/django-audit-log/blob/master/audit_log/middleware.py"""
from django.db.models import signals
from functools import partial


class WhodidMiddleware:
    """
       his class represent as catch request user and mark the user into that model.
       Usage:
        MIDDLEWARE = [
            ....
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'who_created.middleware.WhoDidMiddleware',
            ....
        ]
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated:
                user = request.user
            else:
                user = None
            who_did = partial(self.who_did, user)
            signals.pre_save.connect(who_did, dispatch_uid=(self.__class__, request,), weak=False)

        response = self.get_response(request)

        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))

        return response

    @staticmethod
    def who_did(user, sender, instance, **kwargs):
        """
        :param user:
        :param sender:
        :param instance:
        :param kwargs:
        :return:
        """
        if hasattr(instance, "last_modified_by_id"):
            instance.modified_by = user
        if not getattr(instance, 'created_by_id', None):
            instance.created_by = user

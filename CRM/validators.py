from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User

# file for custom model validators and form validators


def validate_tenant_user(user_id):
    user = User.objects.get(pk=user_id)
    if user.is_landlord:
        raise ValidationError(
            _('%(user)s is not a tenant'),
            params={'user': user},
        )


def validate_landlord_user(user_id):
    user = User.objects.get(pk=user_id)
    if not user.is_landlord:
        raise ValidationError(
            _('%(user)s is not a landlord'),
            params={'user': user},
        )

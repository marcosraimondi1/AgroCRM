from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core import serializers

# validators imports
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# VALIDATORS
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


def validate_billing(billing):
    if (billing.payed + billing.owed) != billing.amount or billing.owed < 0 or billing.payed < 0:
        raise ValidationError(
            _('%(billing)s error'),
            params={'billing': billing},
        )


# MODELS
class User(AbstractUser):
    """
    Users can be either a land owner or a client of a land owner.
    """
    id = models.AutoField(primary_key=True)
    is_landlord = models.BooleanField(default=False)

    def serialize(self):
        if self.is_landlord:

            tenants = []
            for tenant in self.tenants.all():
                tenants.append(tenant.serialize())

            data = {
                "username": self.username,
                "email": self.email,
                "tenants": tenants,
            }

        else:
            data = {
                "username": self.username,
                "email": self.email,
                "landlords": serializers.serialize("json", self.profile.landlords.all(), fields=('username', 'email'))
            }

        return data


class TenantProfile (models.Model):
    id = models.AutoField(primary_key=True)
    # separate table for client information
    tenant = models.OneToOneField(
        User, models.CASCADE, related_name="profile",
        validators=[validate_tenant_user]
    )

    # for client-users -> relate to a owner-users
    # ideally a client can relate with multiple owners and viceversa -> ManyToMany
    landlords = models.ManyToManyField(
        to=User, related_name="tenants", blank=True)

    def __str__(self):
        return f"Tenant {self.tenant.username} "

    def serialize(self):
        data = {
            "username": self.tenant.username,
            "email": self.tenant.email
        }
        return data


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    message = models.CharField('message', max_length=100)
    receiver = models.ForeignKey(
        User, models.CASCADE, related_name="received_messages")
    sender = models.ForeignKey(
        User, models.CASCADE, related_name="sent_messages")
    is_request = models.BooleanField(editable=False, default=False)
    timestamp = models.DateTimeField(auto_now=True)


class Land(models.Model):
    """
    Every owner has zero or many businesses, and every business may have zero or one client.
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField('title', max_length=100)

    description = models.CharField('description', max_length=300)

    # contract = models.FileField(upload_to='contracts/%Y/%m/%d/', blank=True)

    hectares = models.IntegerField('hectares')

    location = models.CharField('location', max_length=100)
    map_link = models.URLField('google maps link')

    lat = models.FloatField('latitude')

    long = models.FloatField('longitude')

    landlord = models.ForeignKey(User, models.CASCADE,
                                 related_name="lands", validators=[validate_landlord_user])

    tenant = models.ForeignKey(
        TenantProfile, models.SET_NULL, related_name='lands', blank=True, verbose_name='tenant', null=True)

    def __str__(self):
        return f"Land {self.pk} owned by {self.landlord.username} "

    def serialize(self):
        try:
            ten = {
                "id": self.tenant.id,
                "username": self.tenant.tenant.username
            }

        except Exception:
            ten = {
                "id": "",
                "username": ""
            }

        data = {
            "title": self.title,
            "description": self.description,
            "hectares": self.hectares,
            "location": self.location,
            # "contract": self.contract.path,
            # "rel_path": self.contract.name,
            "landlord": {
                "id": self.landlord.id,
                "username": self.landlord.username
            },
            "tenant": ten,
            "map": self.map_link,
            "coord": {
                "lat": self.lat,
                "long": self.long
            },
            "billing": {
                "amount": self.billing.amount,
                "payed": self.billing.payed,
                "pending": self.billing.owed,
                "method": self.billing.method,
                "deadline": self.billing.period.strftime("%#d %b %Y"),
                "daysleft": self.billing.daysleft(),
            }
        }
        return data


class Billing(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField('amount')

    payed = models.FloatField('payed', default=0)
    owed = models.FloatField('owed')

    method = models.CharField('mehtod', max_length=100)
    period = models.DateField('period')

    # billing is related to a specific land and a land with a landlord and tenant
    land = models.OneToOneField(
        Land, on_delete=models.CASCADE, verbose_name='land', related_name='billing')

    def __str__(self):
        try:
            return f"{self.land.tenant.tenant.username} owes {self.land.landlord.username} an amount of {self.owed} for land {self.land.id}."
        except:
            return f"Land {self.land.id} for {self.amount}."

    def save(self, *args, **kwargs):
        # initialize/update owed value
        self.owed = self.amount - self.payed

        # Check if billing is valid
        validate_billing(self)
        super().save(*args, **kwargs)

    def daysleft(self):
        today = datetime.date.today()
        return (self.period - today).days

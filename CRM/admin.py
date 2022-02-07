from django.contrib import admin

from .models import User, Land, TenantProfile, Billing, Message

# Register your models here.

admin.site.register(User)
admin.site.register(Land)
admin.site.register(TenantProfile)
admin.site.register(Billing)
admin.site.register(Message)

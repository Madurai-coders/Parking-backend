from django.contrib import admin
from .models import Payment, Booking, Wing, Slots, BusinessPartner

# Register your models here.

admin.site.register(BusinessPartner)
admin.site.register(Payment)
admin.site.register(Booking)
admin.site.register(Wing)
admin.site.register(Slots)
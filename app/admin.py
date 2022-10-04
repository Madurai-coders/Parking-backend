from django.contrib import admin
from .models import Payment, Booking, Table_data, Wing, Slots, BusinessPartner,Table_data,CarInfo,CarInfoTemp,BookingTemp,PaymentEndpoint

# Register your models here.

admin.site.register(BusinessPartner)
admin.site.register(Payment)
admin.site.register(Booking)
admin.site.register(Wing)
admin.site.register(Slots)
admin.site.register(Table_data)
admin.site.register(CarInfo)
admin.site.register(CarInfoTemp)
admin.site.register(BookingTemp)
admin.site.register(PaymentEndpoint)
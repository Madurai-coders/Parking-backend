from .views import AdminCheckAPI,GetBooking,Booked_slots,BusinessPartner_Group,GetBusinessPartner, test,Inactiveslots, GetPayment,GetWing,CreateSlots,CreateWing, CreatePayment,Check_BusinessPartner, CreateBusinessPartner,UserCreateAPIView, CreateBooking
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('CreateBusinessPartner', CreateBusinessPartner, basename='data')
router.register('CreatePayment', CreatePayment, basename='pay')
router.register('CreateBooking', CreateBooking, basename='book')
router.register('CreateWing', CreateWing, basename='wing')
router.register('CreateSlots', CreateSlots, basename='slots')
router.register('Inactiveslots', Inactiveslots, basename='Inactive')
router.register('GetBooking', GetBooking, basename='GetBooking')
router.register('BusinessPartner_Group', BusinessPartner_Group, basename='BusinessPartner_Group')
router.register('GetBusinessPartner', GetBusinessPartner, basename='GetBusinessPartner')


urlpatterns = [
    #path('test', test),
    path('admins/', AdminCheckAPI.as_view(), name='admins'),
    path('Check_BusinessPartner', Check_BusinessPartner.as_view(), name='Check_BusinessPartner'),
    path('GetPayment', GetPayment.as_view(), name='GetPayment'),
    # path('BusinessPartner_Group', BusinessPartner_Group.as_view(), name='BusinessPartner_Group'),
    path('GetWing', GetWing.as_view(), name='GetWing'),
    path('Booked_slots', Booked_slots.as_view(), name='Booked_slots'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('', include(router.urls)),

]

from .views import send_gmail, send_gmail_booking,CreateOnlinePayment, UserLogin,GetUserAccount, GetBookingByDate,SlotCount,AdminCheckAPI,GetBooking,Booked_slots,BusinessPartner_Group,GetBusinessPartner, test,Inactiveslots, GetPayment,GetWing,CreateSlots,CreateWing, CreatePayment,Check_BusinessPartner, CreateBusinessPartner,UserCreateAPIView, CreateBooking
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
router.register('GetBookingByDate', GetBookingByDate, basename='GetBookingByDate')
router.register('BusinessPartner_Group', BusinessPartner_Group, basename='BusinessPartner_Group')
router.register('GetBusinessPartner', GetBusinessPartner, basename='GetBusinessPartner')


urlpatterns = [
    path('admins/', AdminCheckAPI.as_view(), name='admins'),
    path('Check_BusinessPartner', Check_BusinessPartner.as_view(), name='Check_BusinessPartner'),
    path('GetPayment', GetPayment.as_view(), name='GetPayment'),
    path('SlotCount/', SlotCount, name='SlotCount'),
    path('GetWing', GetWing.as_view(), name='GetWing'),
    path('Booked_slots', Booked_slots.as_view(), name='Booked_slots'),
    path('UserLogin', UserLogin.as_view(), name='UserLogin'),
    path('GetUserAccount', GetUserAccount.as_view(), name='GetUserAccount'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('send_mail/', send_gmail, name="send_mail"),
    path('send_mail_booking/', send_gmail_booking, name="send_mail_booking"),
    path('CreateOnlinePayment/4ebd0208-8328-5d69-8c44-ec50939c0967/', CreateOnlinePayment, name="CreateOnlinePayment"),
    path('', include(router.urls)),

]

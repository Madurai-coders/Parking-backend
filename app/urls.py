from .views import UserDataAPIView, test, CreatePayment, CreateBusinessPartner,UserCreateAPIView, CreateBooking
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('data', CreateBusinessPartner, basename='data')
router.register('pay', CreatePayment, basename='pay')
router.register('book', CreateBooking, basename='book')


urlpatterns = [
    #path('test', test),
    path('admins', UserDataAPIView.as_view(), name='admins'),
    path('register', UserCreateAPIView.as_view(), name='register'),
    path('', include(router.urls)),

]

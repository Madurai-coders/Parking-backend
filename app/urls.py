from .views import UserDataViewset, test, PaymentViewset, CreateBusinessAPIview
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('data', PaymentViewset, basename='data')


urlpatterns = [
    path('test', test),
    path('admins', UserDataViewset.as_view(), name='user'),
    path('create', CreateBusinessAPIview.as_view(), name='create'),
    path('', include(router.urls)),

]

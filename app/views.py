from django.db import models
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers, viewsets, generics
from .models import Booking, BusinessPartner, Payment, User
from .serializers import PaymentSerializer, UserSerializer, BusinessSerializer, BookingSerializer

@api_view()
@permission_classes([AllowAny])
def test(request):
    print(request)
    return Response({'message': "hello"})


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserDataAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.all()#filter(id=self.request.user.id)
        return query_set


class CreateBusinessPartner(viewsets.ModelViewSet):
     queryset = BusinessPartner.objects.all()
     serializer_class = BusinessSerializer


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CreateBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer



# class PaymentViewset(viewsets.ModelViewSet):

#     serializer_class = PaymentSerializer
    
#     def get_queryset(self):
#         data = Payment.objects.all()
#         return data
from django.db import models
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated ,IsAdminUser
from rest_framework import serializers, viewsets, generics
from .models import Booking, BusinessPartner, Payment, User,Slots,Wing
from .serializers import PaymentSerializer,BusinessGroup_Serializer, UserSerializer,wingSlotSerializer,SlotSerializer, BusinessSerializer, BookingSerializer,AdminCheckSerializer
from rest_framework import filters
from .pagination import SmallSetPagination,tenSetPagination,fourSetPagination   

@api_view()
@permission_classes([AllowAny])
def test(request):
    print(request)
    return Response({'message': "hello"})


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class AdminCheckAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminCheckSerializer
    permission_classes=[IsAdminUser]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.all()#filter(id=self.request.user.id)
        return query_set




class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class CreateBusinessPartner(viewsets.ModelViewSet):
     permission_classes=[IsAuthenticated]
     queryset = BusinessPartner.objects.all()
     serializer_class = BusinessSerializer


class GetBusinessPartner(viewsets.ModelViewSet):
     permission_classes=[IsAuthenticated]
     queryset = BusinessPartner.objects.all()
     serializer_class = BusinessGroup_Serializer
     pagination_class = tenSetPagination

class Check_BusinessPartner(generics.ListAPIView):
     queryset = BusinessPartner.objects.all()
     serializer_class = BusinessSerializer
     permission_classes=[IsAdminUser]
     filter_backends = [filters.SearchFilter]
     search_fields = ['userName']


class BusinessPartner_Group(viewsets.ModelViewSet):
     queryset = BusinessPartner.objects.all()
     serializer_class = BusinessGroup_Serializer
     permission_classes=[IsAdminUser]
     filter_backends = [filters.SearchFilter]
     search_fields = ['userName']


# ------------------------------------------------------------------------------------------------------------------


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    lookup_field = 'id'



class GetPayment(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes=[IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['paymentId','userId__userName',]
    

class CreateBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class GetBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = self.queryset
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        print(from_date)
        query_set = queryset.filter(endTo__range=[from_date,to_date])
        return query_set




class CreateWing(viewsets.ModelViewSet):
    queryset = Wing.objects.all()
    serializer_class = wingSlotSerializer


class CreateSlots(viewsets.ModelViewSet):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer

class GetWing(generics.ListAPIView):
    queryset = Wing.objects.all()
    serializer_class = wingSlotSerializer
    permission_classes=[IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wingName']


class Inactiveslots(viewsets.ModelViewSet):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(slotStatus=False)
        return query_set

class Booked_slots(generics.ListAPIView):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer

    def get_queryset(self):
        queryset = self.queryset
        id = self.request.query_params.get('id')
        query_set = queryset.filter(slotId=id)
        return query_set    

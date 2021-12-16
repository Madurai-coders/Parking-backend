from django.db import models
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated ,IsAdminUser
from rest_framework import pagination, serializers, viewsets, generics
from .models import Booking, BusinessPartner, Payment, User,Slots,Wing
from .serializers import GetUserSerializer,PaymentSerializer,BusinessGroup_Serializer, UserSerializer,wingSlotSerializer,SlotSerializer, BusinessSerializer, BookingSerializer,AdminCheckSerializer
from rest_framework import filters
from .pagination import SmallSetPagination,tenSetPagination,fourSetPagination   

@api_view()
@permission_classes([AllowAny])
def test(request):
    print(request)
    return Response({'message': "hello"})


@api_view()
@permission_classes([AllowAny])
def SlotCount(request):
    total = Slots.objects.count()
    active = Slots.objects.filter(slotStatus=True).count()
    inactive = Slots.objects.filter(slotStatus=False).count()
    return Response({'total':total,'inactive':inactive,'active':active})



class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class GetUserAccount(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(id=self.request.user.id)
        return query_set

class AdminCheckAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminCheckSerializer
    permission_classes=[IsAuthenticated]

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
     permission_classes=[IsAuthenticated]
     filter_backends = [filters.SearchFilter,filters.OrderingFilter]
     search_fields = ['userName']
     ordering = ('-BusinessPartner_created')
     pagination=tenSetPagination


class BusinessPartner_Group(viewsets.ModelViewSet):
     queryset = BusinessPartner.objects.all()
     serializer_class = BusinessGroup_Serializer
     permission_classes=[IsAuthenticated]
     filter_backends = [filters.SearchFilter]
     search_fields = ['userName']



class UserLogin(generics.ListAPIView):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessGroup_Serializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get('username')
        accountnumber = self.request.query_params.get('accountnumber')
        query_set = queryset.filter(userName=username,accountNumber=accountnumber)
        return query_set

# ------------------------------------------------------------------------------------------------------------------


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class=tenSetPagination
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering = ('-paymentDate')



class GetPayment(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes=[IsAuthenticated]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['paymentId','userId__userName',]
    ordering = ('-paymentDate')
    pagination=tenSetPagination
    

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


class GetBookingByDate(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = self.queryset
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        print(from_date)
        query_set = queryset.filter(date__range=[from_date,to_date])
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
    permission_classes=[IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wingName']


class Inactiveslots(viewsets.ModelViewSet):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]

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

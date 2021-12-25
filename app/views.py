from django.db import models
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import pagination, serializers, viewsets, generics
from .models import Booking, BusinessPartner, Payment, User, Slots, Wing
from .serializers import GetUserSerializer, PaymentSerializer, BusinessGroup_Serializer, UserSerializer, wingSlotSerializer, SlotSerializer, BusinessSerializer, BookingSerializer, AdminCheckSerializer
from rest_framework import filters
from .pagination import SmallSetPagination, tenSetPagination, fourSetPagination
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.template.loader import render_to_string


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
    return Response({'total': total, 'inactive': inactive, 'active': active})


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def send_gmail(request):
    print(request.data["to"])
    messageSent = False
    if request.method == "POST":

        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_mail = settings.EMAIL_HOST_USER  # settings.py
        to_mail = request.POST.get(request.data["to"])  # to must be posted in postman

        msg_html = loader.render_to_string('index.html', {

            'to': request.data["to"],
            'invoiceDate': request.data["invoiceDate"],
            'user': request.data["user"],
            'accountNumber': request.data["accountNumber"],
            'paymentId': request.data["paymentId"],
            'amount':request.data["amount"],
        })

        send_mail(
            subject,
            message,
            from_mail,
            [request.data["to"]],
            fail_silently=False,
            html_message=msg_html,
        )
        messageSent = True

        return Response({"sent": messageSent})

    else:
        return Response({"sent": messageSent})


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def send_gmail_booking(request):
    print(request.data["to"])
    messageSent = False
    if request.method == "POST":

        subject = request.POST.get('subject')
        message = request.POST.get('message')
        from_mail = settings.EMAIL_HOST_USER  # settings.py
        to_mail = request.POST.get(request.data["to"])  # to must be posted in postman

        msg_html = loader.render_to_string('email.html', {

            'to': request.data["to"],
            'invoiceDate': request.data["invoiceDate"],
            'user': request.data["user"],
            'accountNumber': request.data["accountNumber"],
            'bookingId': request.data["bookingId"],
            'amount':request.data["amount"],
            'startFrom':request.data["startFrom"],
            'endTo':request.data["endTo"],
            'wing':request.data["wing"],
            'slot':request.data["slot"],
            'plan':request.data["plan"],
            'id':request.data["id"],
        })

        send_mail(
            subject,
            message,
            from_mail,
            [request.data["to"]],
            fail_silently=False,
            html_message=msg_html,
        )
        messageSent = True

        return Response({"sent": messageSent})

    else:
        return Response({"sent": messageSent})




class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class GetUserAccount(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = GetUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(id=self.request.user.id)
        return query_set


class AdminCheckAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AdminCheckSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.all()  # filter(id=self.request.user.id)
        return query_set


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]



class CreateBusinessPartner(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessSerializer


class GetBusinessPartner(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessGroup_Serializer
    pagination_class = tenSetPagination


class Check_BusinessPartner(generics.ListAPIView):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['userName']
    ordering = ('-BusinessPartner_created')
    pagination = tenSetPagination


class BusinessPartner_Group(viewsets.ModelViewSet):
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessGroup_Serializer
    permission_classes = [IsAdminUser]
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
        query_set = queryset.filter(
            userName=username, accountNumber=accountnumber)
        return query_set

# ------------------------------------------------------------------------------------------------------------------


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = tenSetPagination
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering = ('-paymentDate')
    permission_classes=[IsAdminUser]



@api_view(['POST'])
@permission_classes([AllowAny])
def CreateOnlinePayment(request):
    if request.method == 'POST':
        if request.data["secretKey"]=='9401f9e0-6596-11ec-bd15-8d09a4545895':
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GetPayment(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paymentId', 'userId__userName', ]
    ordering = ('-paymentDate')
    pagination = tenSetPagination


class CreateBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('-date_auto')
    permission_classes = [IsAdminUser]



class GetBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        queryset = self.queryset
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        print(from_date)
        query_set = queryset.filter(
            endTo__range=[from_date, to_date]).order_by('-date_auto')
        return query_set


class GetBookingByDate(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('-date_auto')
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        queryset = self.queryset
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        print(from_date)
        query_set = queryset.filter(
            date__range=[from_date, to_date]).order_by('-date_auto')
        return query_set


class CreateWing(viewsets.ModelViewSet):
    queryset = Wing.objects.all()
    serializer_class = wingSlotSerializer
    permission_classes = [IsAdminUser]


class CreateSlots(viewsets.ModelViewSet):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAdminUser]


class GetWing(generics.ListAPIView):
    queryset = Wing.objects.all()
    serializer_class = wingSlotSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wingName']


class Inactiveslots(viewsets.ModelViewSet):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(slotStatus=False)
        return query_set


class Booked_slots(generics.ListAPIView):
    queryset = Slots.objects.all()
    serializer_class = SlotSerializer
    permission_classes = [IsAdminUser]


    def get_queryset(self):
        queryset = self.queryset
        id = self.request.query_params.get('id')
        query_set = queryset.filter(slotId=id)
        return query_set

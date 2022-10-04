from django.http import HttpResponse
import datetime
from cgitb import lookup
from django.db import models
from django.db.models.query import QuerySet
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import pagination, serializers, viewsets, generics
from .models import Booking, BusinessPartner, Payment, User, Slots, Wing, Table_data,CarInfo,CarInfoTemp,BookingTemp,PaymentEndpoint
from .serializers import GetUserSerializer,PaymentEndpointSerializer,TableDataSerializer,CarInfoTempSerializer,BookingTempSerializer,CarInfoSerializer,PaymentSerializer,UserSerializer_verified,BusinessGroup_Serializer, UserSerializer, wingSlotSerializer, SlotSerializer, BusinessSerializer, BookingSerializer, AdminCheckSerializer
from rest_framework import filters
from .pagination import SmallSetPagination, tenSetPagination, fourSetPagination
from rest_framework import status

from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template import loader
from django.template.loader import render_to_string


@api_view()
@permission_classes([AllowAny])
def test(request):
    print(request)
    return Response({'message': "hello"})


@api_view()
@permission_classes([IsAuthenticated])
def SlotCount(request):
    total = Slots.objects.count()
    active = Slots.objects.filter(slotStatus=True).count()
    inactive = Slots.objects.filter(slotStatus=False).count()
    return Response({'total': total, 'inactive': inactive, 'active': active})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def send_gmail(request):
    print(request.data["to"])
    messageSent = False
    if request.method == "POST":

        subject = 'ZenGov Payment'
        message = request.POST.get('message')
        from_mail = settings.EMAIL_HOST_USER  # settings.py
        # to must be posted in postman
        to_mail = request.POST.get(request.data["to"])

        msg_html = loader.render_to_string('index.html', {

            'to': request.data["to"],
            'invoiceDate': request.data["invoiceDate"],
            'user': request.data["user"],
            'accountNumber': request.data["accountNumber"],
            'paymentId': request.data["paymentId"],
            'amount': request.data["amount"],
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


# @api_view(['PUT','GET'])
# @permission_classes([AllowAny])
def verification_email(request,user_name,mobile_number):
    print(user_name)
    now = datetime.datetime.now()
    msg = f'Today is {now}'
    return HttpResponse(msg, content_type='text/plain')
    # queryset = BusinessPartner.objects.all()
    # serializer = BusinessGroup_Serializer(queryset, many=True)
    # serializer.data


from django.http import HttpResponse  
from django.shortcuts import render, redirect  
from django.contrib.auth import login, authenticate  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_text  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  
from .models import  User
 

def activate(request, uidb64, token):  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return render(request, "verificationSuccessful.html") 
    else:  
        return HttpResponse('Activation link is invalid!')  



# @api_view(['GET', 'POST'])
# @permission_classes([AllowAny])
# def send_verification_email(request):
#     print(request.data["to"])
#     messageSent = False
#     if request.method == "POST":

#         subject = 'ZenGov Payment'
#         message = request.POST.get('message')
#         from_mail = settings.EMAIL_HOST_USER
#         to_mail = request.POST.get(request.data["to"])
#         msg_html = loader.render_to_string('verifyemail.html', {
#             'link': request.data["link"],
#         })

#         send_mail(
#             subject,
#             message,
#             from_mail,
#             [request.data["to"]],
#             fail_silently=False,
#             html_message=msg_html,
#         )
#         messageSent = True

#         return Response({"sent": messageSent})

#     else:
#         return Response({"sent": messageSent})


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def send_gmail_booking(request):
    print(request.data["to"])
    messageSent = False
    if request.method == "POST":

        subject = 'ZenGov Booking'
        message = request.POST.get('message')
        from_mail = settings.EMAIL_HOST_USER  # settings.py
        # to must be posted in postman
        to_mail = request.POST.get(request.data["to"])

        msg_html = loader.render_to_string('email.html', {

            'to': request.data["to"],
            'invoiceDate': request.data["invoiceDate"],
            'user': request.data["user"],
            'accountNumber': request.data["accountNumber"],
            'bookingId': request.data["bookingId"],
            'amount': request.data["amount"],
            'startFrom': request.data["startFrom"],
            'endTo': request.data["endTo"],
            'wing': request.data["wing"],
            'slot': request.data["slot"],
            'plan': request.data["plan"],
            'id': request.data["id"],
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
@permission_classes([IsAdminUser])
def email_with_attachment(request, *args, **kwargs):
    if request.method == "POST":
        # file_path = os.path.abspath('media/bg-2.jpg')
        print(request.data["to"])
        msg = EmailMessage(request.data["name"],
                           request.data["description"], to=[request.data["to"]])
        msg.attach('ZenGov_Parking_data.csv', request.data["csv"], 'text/csv')
        msg.send()
        return Response('true')


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserCreateAPIViewVerified(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer_verified
    permission_classes = (AllowAny,)
    
 
class CarInfoView(generics.CreateAPIView):
    queryset = CarInfo.objects.all()
    serializer_class = CarInfoSerializer
    permission_classes = [IsAuthenticated]
    
class CarInfoTempView(viewsets.ModelViewSet):
    queryset = CarInfoTemp.objects.all()
    serializer_class = CarInfoTempSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'

    
class BookingTempView(viewsets.ModelViewSet):
    queryset = BookingTemp.objects.all()
    serializer_class = BookingTempSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'key'
    
class PaymentEndpointView(viewsets.ModelViewSet):
    queryset = PaymentEndpoint.objects.all()
    serializer_class = PaymentEndpointSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'transNum'
    
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
        query_set = queryset.all().filter(id=self.request.user.id)
        return query_set


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]


class TableData(viewsets.ModelViewSet):
    queryset = Table_data.objects.all()
    serializer_class = TableDataSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'table_name'


class CreateBusinessPartner(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessSerializer
    permission_classes = [IsAuthenticated]

class GetBusinessPartner(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = BusinessPartner.objects.all()
    serializer_class = BusinessGroup_Serializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('-BusinessPartner_created')
    pagination_class = tenSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ('-BusinessPartner_created')


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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(accountHolder=self.request.user.id)
        return query_set

# ------------------------------------------------------------------------------------------------------------------


class CreatePayment(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    pagination_class = tenSetPagination
    lookup_field = 'id'
    filter_backends = [filters.OrderingFilter]
    ordering = ('-paymentDate')
    permission_classes = [IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateOnlinePayment(request):
    if request.method == 'POST':
        if request.data["secretKey"] == '9401f9e0-6596-11ec-bd15-8d09a4545895':
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetPayment(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['paymentId', 'userId__userName', ]
    ordering = ('-paymentDate')
    pagination = tenSetPagination


class GetPaymentbyDate(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.queryset
        from_date = self.request.query_params.get('from')
        to_date = self.request.query_params.get('to')
        print(from_date)
        query_set = queryset.filter(
            paymentDate__range=[from_date, to_date]).order_by('-paymentDate')
        return query_set


class CreateBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('-date_auto')
    permission_classes = [IsAuthenticated]


class GetBooking(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]


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
    ordering = ('-date_auto')
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

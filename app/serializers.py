from django.contrib.auth.models import User
from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Booking, BusinessPartner, Payment, Slots, User, Wing, Table_data, CarInfo


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff', 'id')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer_verified(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'is_staff', 'id', 'is_active', 'first_name')

    def create(self, validated_data):
        print(validated_data)
        user = super(UserSerializer_verified, self).create(validated_data)
        user.is_active = False
        user.set_password(validated_data['password'])
        print(user.pk)
        user.save()
        # current_site = get_current_site(validated_data['request'])
        subject = 'ZenGov parking mail verification'
        message = 'please confirm your mail address'
        from_mail = settings.EMAIL_HOST_USER  # settings.py
        # to must be posted in postman
        msg_html = loader.render_to_string('verifyemail.html', {
            'user': user.first_name,
            'domain': 'http://127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })

        send_mail(
            subject,
            message,
            from_mail,
            [user],
            fail_silently=False,
            html_message=msg_html,
        )

        return user


class AdminCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff']


class TableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table_data
        fields = '__all__'


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessPartner
        fields = ['id', 'uId', 'accountNumber', 'userName',
                  'lastName', 'email', 'accountHolder','mobileNumber']

        # must be serializers.ModelSerializer not serializers.Serializer


class PaymentSerializer(serializers.ModelSerializer):
    User = BusinessSerializer(source='userId', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'userId', 'paymentId', 'amount',
                  'paymentType', 'paymentDate', 'User']


class WingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wing
        fields = ('wingId', 'wingName', 'wingStatus')


class SlotSerializer(serializers.ModelSerializer):
    wing = WingSerializer(source='wingId', read_only=True)

    class Meta:
        model = Slots
        fields = ('id', 'slotId', 'slotStatus', 'wingId', 'wing')


class wingSlotSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)

    class Meta:
        model = Wing
        fields = '__all__'
        depth = 1


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    booking_link = CarInfoSerializer(read_only=True)
    User = BusinessSerializer(source='userId', read_only=True)
    slots = SlotSerializer(source='slot_connect', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'userId', 'bookingId', 'date', 'startFrom', 'endTo', 'plan',
                  'slotid', 'charge', 'slot_connect', 'User', 'slots', 'booking_link']


class BusinessGroup_Serializer(serializers.ModelSerializer):
    payment_partner = PaymentSerializer(many=True, read_only=True)
    booking_partner = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = BusinessPartner
        fields = ['id', 'uId', 'accountNumber', 'userName',
                  'lastName', 'email', 'payment_partner', 'booking_partner','mobileNumber']
        depth = 1


class GetUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    userData = BusinessGroup_Serializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'useraccount',
                  'password', 'userData', 'first_name')
        depth = 2

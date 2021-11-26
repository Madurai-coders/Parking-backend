from django.core.exceptions import FieldError
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Booking, BusinessPartner, Payment, Slots, User, Wing


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPartner
        fields = ['uId', 'accountNumber', 'userName',
                  'lastName', 'email', 'accountHolder']


                                                                    # must be serializers.ModelSerializer not serializers.Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'userId', 'accountNumber', 'paymentId',
                  'paymentType', 'paymentDateTime']
    

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['userId', 'bookingId', 'date', 'startFrom', 'endTo', 'plan']


class WingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wing
        fields = ['wingId', 'wingName', 'wingStatus']

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slots
        fields = ['slotId','slotStatus','wingStatus']
from django.core.exceptions import FieldError
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Booking, BusinessPartner, Payment, Slots, User, Wing,Table_data


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







class AdminCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','is_staff']


class TableDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table_data
        fields = '__all__'





        


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = BusinessPartner
        fields = ['id','uId', 'accountNumber', 'userName',
                  'lastName', 'email']





                                                                    # must be serializers.ModelSerializer not serializers.Serializer
class PaymentSerializer(serializers.ModelSerializer):
    User = BusinessSerializer(source='userId',read_only=True)
    class Meta:
        model = Payment
        fields = ['id','userId', 'paymentId', 'amount',
                  'paymentType', 'paymentDate','User' ]
    




class WingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wing
        fields = ('wingId', 'wingName', 'wingStatus')
class SlotSerializer(serializers.ModelSerializer):
    wing = WingSerializer(source='wingId',read_only=True)
    class Meta:
        model = Slots
        fields = ('id','slotId','slotStatus','wingId','wing')


class wingSlotSerializer(serializers.ModelSerializer):
    slots = SlotSerializer(many=True, read_only=True)
    class Meta:
        model = Wing
        fields = '__all__'
        depth = 1


class BookingSerializer(serializers.ModelSerializer):
    User = BusinessSerializer(source='userId',read_only=True)
    slots = SlotSerializer(source='slot_connect',read_only=True)
    class Meta:
        model = Booking
        fields = ['id','userId', 'bookingId', 'date', 'startFrom', 'endTo', 'plan','slotid','charge','slot_connect','User','slots']

class BusinessGroup_Serializer(serializers.ModelSerializer):
    payment_partner = PaymentSerializer(many=True, read_only=True)
    booking_partner = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = BusinessPartner
        fields = ['id','uId', 'accountNumber', 'userName',
                  'lastName', 'email','payment_partner','booking_partner']
        depth = 1


class GetUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id','username','useraccount','password')

from django.db import models
from django.contrib.auth.models import User




#Create your models here.
class BusinessPartner(models.Model):
    uId = models.IntegerField()
    accountNumber = models.CharField(max_length=12)
    userName = models.CharField(max_length=12)
    lastName = models.CharField(max_length=12)
    email = models.EmailField()
    accountHolder = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE )

    def __str__(self):
        return str(self.userName)


class Payment(models.Model):
    userId = models.ForeignKey(BusinessPartner, default=1, on_delete=models.CASCADE)
    accountNumber = models.IntegerField()
    paymentId = models.CharField(max_length=12)
    paymentType = models.CharField(max_length=10)
    paymentDateTime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.userId)


class Booking(models.Model):
    userId = models.ForeignKey(BusinessPartner, default=1, on_delete=models.CASCADE)
    bookingId = models.IntegerField()
    date = models.DateTimeField(auto_now=True)
    startFrom = models.DateField()
    endTo = models.DateField()
    plan = models.CharField(max_length=18)   #plan weekly, monthly, quaterly, yearly

    def __str__(self):
        return str(self.userId)


class Wing(models.Model): #slot a,b,c
    wingId = models.IntegerField()
    wingName = models.CharField(max_length=10)  #slot A, slot B
    wingStatus = models.BooleanField()
    
    def __str__(self):
        return str(self.wingName)


class Slots(models.Model):
    slotId = models.IntegerField()
    slotStatus = models.BooleanField()
    wingId = models.ForeignKey(Wing, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.slotId)
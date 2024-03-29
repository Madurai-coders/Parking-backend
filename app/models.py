from django.db import models
from django.contrib.auth.models import User




#Create your models here.
class BusinessPartner(models.Model):
    uId = models.CharField(max_length=120)
    accountNumber = models.CharField(max_length=120)
    userName = models.CharField(max_length=120)
    lastName = models.CharField(max_length=120)
    email = models.EmailField()
    accountHolder = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE ,related_name='useraccount')
    BusinessPartner_created = models.DateTimeField(auto_now=True)
    mobileNumber=models.IntegerField(blank=True, null=True)
    
    def __str__(self):
        return str(self.userName)


class Payment(models.Model):
    userId = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE,related_name='payment_partner')
    paymentId = models.CharField(max_length=120)
    paymentType = models.CharField(max_length=100)
    paymentDate = models.CharField(max_length=100)
    Status = models.CharField(max_length=100,default='failed')
    key = models.CharField(max_length=100,default='fai-led')
    amount = models.IntegerField()
    paymentDateTime_auto = models.DateTimeField(auto_now=True,blank=True, null=True)

    class Meta:
        ordering = ['-paymentDate']

    def __str__(self):
        return str(self.paymentId)



class Wing(models.Model): #slot a,b,c
    wingId = models.CharField(max_length=100)
    wingName = models.CharField(max_length=100) 
    wingCount = models.IntegerField() #slot A, slot B
    wingStatus = models.BooleanField()
    planDaily = models.IntegerField(default=0)
    planWeekly = models.IntegerField()
    planMonthly = models.IntegerField()
    planQuarterly = models.IntegerField()
    planYearly = models.IntegerField()

    def __str__(self):
        return str(self.wingName)


class Slots(models.Model):
    slotId = models.CharField(max_length=100)
    slotStatus = models.BooleanField()
    wingId = models.ForeignKey(Wing, related_name='slots', on_delete=models.CASCADE )
    date_auto = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slotId)


class Booking(models.Model):
    userId = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE,related_name='booking_partner')
    bookingId = models.CharField(max_length=120)
    date_auto = models.DateTimeField(auto_now=True)
    date = models.CharField(max_length=120)
    startFrom = models.CharField(max_length=120)
    endTo = models.CharField(max_length=120)
    slotid = models.CharField(max_length=120)
    slot_connect = models.ForeignKey(Slots,on_delete=models.CASCADE,related_name='slots')
    plan = models.CharField(max_length=120)   #plan weekly, monthly, quaterly, yearly
    charge = models.CharField(max_length=120)  

    class Meta:
        ordering = ['-date_auto']

    def __str__(self):
        return str(self.bookingId)


class CarInfo(models.Model):
    bookingId = models.OneToOneField(Booking,on_delete=models.CASCADE ,related_name='booking_link')
    license = models.CharField(max_length=120)
    make = models.CharField(max_length=120)
    model = models.IntegerField()
    carRegistrationState = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    insurance = models.CharField(max_length=120)
    permitYear = models.CharField(max_length=120)
  
    
    def __str__(self):
        return str(self.license)


class BookingTemp(models.Model):
    userId = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE,)
    bookingId = models.CharField(max_length=120)
    date_auto = models.DateTimeField(auto_now=True)
    date = models.CharField(max_length=120)
    startFrom = models.CharField(max_length=120)
    endTo = models.CharField(max_length=120)
    slotid = models.CharField(max_length=120)
    slot_connect = models.ForeignKey(Slots,on_delete=models.CASCADE)
    plan = models.CharField(max_length=120)   #plan weekly, monthly, quaterly, yearly
    charge = models.CharField(max_length=120)  
    key = models.CharField(max_length=120)  

    class Meta:
        ordering = ['-date_auto']

    def __str__(self):
        return str(self.bookingId)


class CarInfoTemp(models.Model):
    bookingId = models.OneToOneField(BookingTemp,on_delete=models.CASCADE)
    license = models.CharField(max_length=120)
    make = models.CharField(max_length=120)
    model = models.IntegerField()
    carRegistrationState = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    insurance = models.CharField(max_length=120)
    permitYear = models.CharField(max_length=120)
    key = models.CharField(max_length=120)  

  
    
    def __str__(self):
        return str(self.license)


class Table_data(models.Model):
    table_name = models.CharField(max_length=120)
    table_data = models.CharField(max_length=120,null=True)
    
    def __str__(self):
        return str(self.table_name)

class PaymentEndpoint(models.Model):
    status = models.CharField(max_length=120)
    transNum = models.CharField(max_length=120,null=True)
    serviceType = models.CharField(max_length=120,null=True)
    def __str__(self):
        return str(self.transNum)
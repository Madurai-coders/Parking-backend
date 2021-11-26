from django.db.models.query import QuerySet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import serializers, viewsets, generics
from .models import BusinessPartner, Payment, User
from .serializers import PaymentSerializer, UserSerializer, BusinessSerializer

@api_view()
@permission_classes([AllowAny])
def test(request):
    print(request)
    return Response({'message': "hello"})


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserDataViewset(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(id=self.request.user.id)
        return query_set

class CreateBusinessAPIview(generics.CreateAPIView):
    queryset = BusinessPartner.objects.all()
    serializer_class  = BusinessSerializer

 

    





class PaymentViewset(viewsets.ModelViewSet):

    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        data = Payment.objects.all()
        return data
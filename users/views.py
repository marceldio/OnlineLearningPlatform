from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer
from users.filters import PaymentFilter  # Создадим этот фильтр


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ['payment_date']  # Сортировка по дате оплаты
    ordering = ['-payment_date']  # По умолчанию сортировка от новых к старым


class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

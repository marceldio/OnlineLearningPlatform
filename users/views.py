from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from lms.models import Course, Lesson
from users.filters import PaymentFilter
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer
from users.services.stripe_service import (convert_rub_to_dollars,
                                           create_stripe_checkout_session,
                                           create_stripe_price,
                                           create_stripe_product)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter


class PaymentAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user

        # Получаем данные из запроса: курс или урок
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")

        # Проверяем, для чего создается платеж — для курса или урока
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            product_item = course
            amount = course.price
        elif lesson_id:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            product_item = lesson
            amount = lesson.price
        else:
            return Response(
                {
                    "detail": "Необходимо указать либо курс, либо урок для создания платежа."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Сохранить платеж в базе данных
        payment = Payment.objects.create(
            user=user,
            paid_course=course if course_id else None,
            paid_lesson=lesson if lesson_id else None,
            amount=amount,
            payment_method=request.data.get(
                "payment_method", "cash"
            ),  # Добавлено для указания способа оплаты
        )

        # Создать продукт в Stripe для курса или урока
        product_id = create_stripe_product(payment=payment)

        # Конвертация суммы в доллары
        amount_in_dollars = convert_rub_to_dollars(payment.amount)

        # Создать цену в Stripe
        price_id = create_stripe_price(product_id, amount_in_dollars)

        # Создать сессию оплаты в Stripe
        success_url = "https://127.0.0.1:8000/lms/"
        cancel_url = "https://127.0.0.1:8000/users/create-payment/"
        session_id, payment_link = create_stripe_checkout_session(
            price_id, success_url, cancel_url
        )

        # Обновляем платеж данными о Stripe
        payment.stripe_session_id = session_id
        payment.link = payment_link
        payment.save()

        return Response({"payment_url": payment_link}, status=status.HTTP_200_OK)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserProfileView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


# Наследуемся от стандартного сериализатора для добавления возможности входа по email
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Можно добавить кастомные поля, если нужно
        token["email"] = user.email
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

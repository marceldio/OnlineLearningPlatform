from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from lms.models import Course, Lesson
from users.models import Payment, User


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "title", "description"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "video"]


class PaymentSerializer(serializers.ModelSerializer):
    payment_method = serializers.ChoiceField(choices=Payment.PAYMENT_METHODS)
    paid_course = CourseSerializer(read_only=True)
    paid_lesson = LessonSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "password", "phone", "city", "payment_history"]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Чтобы пароль был скрытым при выводе

    def create(self, validated_data):
        # Хешируем пароль перед сохранением пользователя
        user = User(
            email=validated_data["email"],
            phone=validated_data.get("phone"),
            city=validated_data.get("city"),
        )
        user.set_password(validated_data["password"])  # Хешируем пароль
        user.save()
        return user

    def get_payment_history(self, obj):
        payments = Payment.objects.filter(user=obj)
        return PaymentSerializer(payments, many=True).data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Меняем валидацию так, чтобы аутентификация происходила по email
        try:
            user = User.objects.get(email=attrs["email"])
            if user.check_password(attrs["password"]):
                return super().validate(attrs)
            else:
                raise ValidationError({"password": "Invalid password"})
        except User.DoesNotExist:
            raise ValidationError({"email": "User with this email does not exist"})

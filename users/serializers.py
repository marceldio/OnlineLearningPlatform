from rest_framework import serializers

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
        fields = ["id", "email", "phone", "city", "payment_history"]

    def get_payment_history(self, obj):
        payments = Payment.objects.filter(user=obj)
        return PaymentSerializer(payments, many=True).data

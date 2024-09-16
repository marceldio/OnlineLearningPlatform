from rest_framework import serializers
from users.models import User, Payment
from lms.models import Course, Lesson


# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = ['id', 'title']
#
# class LessonSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ['id', 'title']
#
# class PaymentSerializer(serializers.ModelSerializer):
#     paid_course = CourseSerializer(source='paid_course', read_only=True)
#     paid_lesson = LessonSerializer(source='paid_lesson', read_only=True)
#
#     class Meta:
#         model = Payment
#         fields = ['id', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']
#
# class UserProfileSerializer(serializers.ModelSerializer):
#     payment_history = serializers.SerializerMethodField()
#
#     class Meta:
#         model = User
#         fields = ['id', 'email', 'phone', 'city', 'payment_history']
#
#     def get_payment_history(self, obj):
#         payments = Payment.objects.filter(user=obj)
#         return PaymentSerializer(payments, many=True).data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_date', 'amount']  # Уберите связанные поля   #, 'payment_method'

class UserProfileSerializer(serializers.ModelSerializer):
    payment_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'payment_history']

    def get_payment_history(self, obj):
        payments = Payment.objects.filter(user=obj)
        return PaymentSerializer(payments, many=True).data

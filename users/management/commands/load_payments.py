from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    help = "Load payment data"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        user1 = User.objects.get(pk=1)
        user2 = User.objects.get(pk=2)
        course = Course.objects.get(pk=1)
        lesson = Lesson.objects.get(pk=1)

        Payment.objects.create(
            user=user1,
            payment_date=datetime(2024, 9, 16, 21, 0),
            paid_course=course,
            amount=1000.00,
            payment_method="cash",
        )

        Payment.objects.create(
            user=user2,
            payment_date=datetime(2024, 9, 16, 19, 0),
            paid_course=course,
            amount=1000.00,
            payment_method="cash",
        )

        Payment.objects.create(
            user=user2,
            payment_date=datetime(2024, 9, 17, 1, 0),
            paid_lesson=lesson,
            amount=500.00,
            payment_method="transfer",
        )

        self.stdout.write(self.style.SUCCESS("Successfully loaded payment data"))

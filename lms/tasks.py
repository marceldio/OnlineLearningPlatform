from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from lms.models import Course, Lesson

@shared_task
def send_course_update_email(course_id, user_ids):
    course = Course.objects.get(id=course_id)
    users = User.objects.filter(id__in=user_ids)

    for user in users:
        send_mail(
            f'Обновление курса: {course.title}',
            f'Курс "{course.title}" был обновлён. Проверьте новые материалы!',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

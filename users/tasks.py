from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def block_inactive_users():
    # Определяем дату, когда пользователи должны были последним раз войти
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим всех активных пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    # Блокируем этих пользователей
    inactive_users.update(is_active=False)

    return f"{inactive_users.count()} пользователей были заблокированы за неактивность."

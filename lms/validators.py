from django.core.exceptions import ValidationError
from urllib.parse import urlparse

ALLOWED_DOMAINS = ["youtube.com", "youtu.be"]

def validate_youtube_url(value):
    print(f"Validating URL: {value}")  # Временный вывод для проверки
    parsed_url = urlparse(value)
    domain = parsed_url.netloc
    if not any(allowed_domain in domain for allowed_domain in ALLOWED_DOMAINS):
        raise ValidationError('Вам разрешено добавлять ссылки только с youtube.com или youtu.be')


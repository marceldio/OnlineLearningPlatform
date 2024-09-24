from rest_framework.test import APITestCase
from lms.models import Lesson, Course
from lms.serializers import LessonSerializer

class LessonSerializerTestCase(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(title='Test Course', description='Test description')

        self.valid_data = {
            'title': 'Valid YouTube Lesson',
            'content': 'This is a lesson with a valid YouTube video.',
            'video': 'https://www.youtube.com/watch?v=abcd1234',
            'course': self.course.id
        }
        self.invalid_data = {
            'title': 'Invalid Lesson',
            'content': 'This lesson has an invalid video URL.',
            'video': 'https://www.vimeo.com/video/1234',
            'course': self.course.id
        }

    def test_valid_youtube_url(self):
        serializer = LessonSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['video'], self.valid_data['video'])

    def test_invalid_url(self):
        serializer = LessonSerializer(data=self.invalid_data)
        is_valid = serializer.is_valid()  # Вызываем is_valid()
        print("Validation errors (invalid_data):", serializer.errors)  # Для отладки
        self.assertFalse(is_valid)  # Проверяем, что данные невалидные
        self.assertIn('video', serializer.errors)  # Проверяем, что поле 'video' содержит ошибки
        self.assertEqual(serializer.errors['video'][0], 'Вам разрешено добавлять ссылки только с youtube.com или youtu.be')

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'lesson_count']  # Добавляем поле lesson_count

    # Метод для получения количества уроков
    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

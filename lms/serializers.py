from rest_framework import serializers
from lms.models import Lesson, Course
from lms.validators import validate_youtube_url

class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=[validate_youtube_url])
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "video",
            "course",
            "owner",
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # Вложенный сериализатор для уроков
    lessons_count = serializers.SerializerMethodField()  # Поле для вывода количества уроков

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lessons", "lessons_count"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()  # Возвращаем количество уроков, связанных с курсом


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Вложенные уроки

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "owner", "lessons"]

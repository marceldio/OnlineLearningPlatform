from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
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
        ref_name = "LMS_LessonSerializer"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # Вложенный сериализатор для уроков
    lessons_count = (
        serializers.SerializerMethodField()
    )  # Поле для вывода количества уроков
    is_subscribed = serializers.SerializerMethodField()  # Поле для отображения подписки

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "preview",
            "lessons",
            "lessons_count",
            "is_subscribed",
        ]
        ref_name = "LMS_CourseSerializer"

    def get_lessons_count(self, obj):
        return obj.lessons.count()  # Возвращаем количество уроков, связанных с курсом

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False


class CourseDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Вложенные уроки

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "owner", "lessons"]

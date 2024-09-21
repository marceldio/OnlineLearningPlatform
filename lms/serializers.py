from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "video",
            "course",
            "owner",
        ]  # Указываем нужные поля урока


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(
        many=True, read_only=True
    )  # Вложенный сериализатор для уроков
    lessons_count = SerializerMethodField()  # Поле для вывода количества уроков

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "lessons", "lessons_count"]

    def get_lessons_count(self, obj):
        return obj.lessons.count()  # Возвращаем количество уроков, связанных с курсом


class CourseDetailSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)  # Вложенные уроки

    class Meta:
        model = Course
        fields = ["id", "title", "description", "preview", "owner", "lessons"]

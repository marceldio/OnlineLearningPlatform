from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePagination, LessonPagination
from lms.serializers import CourseDetailSerializer, CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePagination  # Добавляем пагинацию

    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        # Модераторы не могут создавать курсы, эта функция будет недоступна для них
        serializer.save(owner=self.request.user)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                ~IsModer,
            )  # Создание доступно только не модераторам
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (
                IsModer | IsOwner,
            )  # Обновление и чтение доступно модераторам или владельцам
        elif self.action == "destroy":
            self.permission_classes = (
                ~IsModer | IsOwner,
            )  # Удаление доступно владельцам, не модераторам
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [
        IsAuthenticated
    ]  # Убедимся, что только аутентифицированные пользователи могут создавать

    def post(self, request, *args, **kwargs):
        # Добавляем проверку внутри
        if request.user.groups.filter(name="moders").exists():
            return Response(
                {"detail": "Модераторы не могут создавать уроки."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Список уроков - доступен для модераторов для чтения
class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all().order_by("id")  # Добавляем сортировку
    serializer_class = LessonSerializer
    pagination_class = LessonPagination
    permission_classes = (IsModer | IsOwner,)


class LessonRetrieveUpdateApiView(RetrieveUpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )  # Модераторы и владельцы могут обновлять и просматривать


# Удаление уроков - модераторы не могут удалять уроки
class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, *args, **kwargs):
        lesson = self.get_object()
        print(f"User: {request.user}, Owner: {lesson.owner}")
        return super().delete(request, *args, **kwargs)


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)

        # Получаем подписку пользователя на курс, если она существует
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()  # Удаляем подписку
            message = "Подписка удалена"
        else:
            Subscription.objects.create(
                user=user, course=course_item
            )  # Создаем подписку
            message = "Подписка добавлена"

        return Response({"message": message})

from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson
from lms.serializers import (CourseDetailSerializer, CourseSerializer,
                             LessonSerializer)
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

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


# Создание уроков - модераторы не могут создавать уроки
class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# Список уроков - доступен для модераторов для чтения
class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsModer | IsOwner,
    )  # Просмотр доступен модераторам и владельцам


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
    permission_classes = (
        IsAuthenticated,
        IsOwner,
        ~IsModer,
    )  # Могут удалять только владельцы

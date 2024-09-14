from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    preview = models.ImageField(
        upload_to="lms/course", verbose_name="Превью", blank=True, null=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Название урока")
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    preview = models.ImageField(
        upload_to="lms/lesson", verbose_name="Превью", blank=True, null=True
    )
    video = models.FileField(
        upload_to="lms/videos", verbose_name="Видео", blank=True, null=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

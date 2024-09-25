from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LMSAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@test.com", password="password123"
        )
        self.assertFalse(
            self.owner.groups.filter(name="moders").exists()
        )  # Проверяем, что owner не модератор
        self.moderator = User.objects.create_user(
            email="moderator@test.com", password="password123", is_staff=True
        )
        self.user = User.objects.create_user(
            email="user@test.com", password="password123"
        )

        # Создаем группу "moders" и добавляем модератора в нее
        moders_group, created = Group.objects.get_or_create(name="moders")
        moders_group.user_set.add(self.moderator)

        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
            owner=self.owner,
            video="https://www.youtube.com/watch?v=testvideo",
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lessons_create")
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "video": "https://www.youtube.com/watch?v=abcd1234",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.owner)
        url = reverse("lms:lessons_retrieve_update", kwargs={"pk": self.lesson.id})
        data = {
            "title": "Updated Lesson Title",
            "description": "Updated Lesson Description",
            "video": "https://www.youtube.com/watch?v=updatedvideo",
            "course": self.course.id,
        }
        response = self.client.put(url, data, format="json")

        print(f"Response status code: {response.status_code}")
        print(f"Response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson Title")

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(
            self.lesson.owner, self.owner
        )  # Проверяем, что пользователь действительно владелец
        url = reverse("lms:lessons_delete", kwargs={"pk": self.lesson.id})
        response = self.client.delete(url)

        print(f"Response status code: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("lms:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_unsubscribe_from_course(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse("lms:subscribe")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("lms:lessons_create")
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
            "video": "https://www.youtube.com/watch?v=abcd1234",
        }
        response = self.client.post(url, data, format="json")

        print(f"Response status code: {response.status_code}")
        print(f"Moderator: {self.moderator.groups.filter(name='moders').exists()}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

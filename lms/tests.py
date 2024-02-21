from django.urls import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='123qwe456rty')
        self.client.force_authenticate(user=self.user)
        self.title = 'Тестовый урок'
        self.description = 'Тестовое описание'
        self.video_link = 'https://www.youtube.com/'
        self.course = Course.objects.create(title='Тестовый курс', description='Тестовое описание')
        self.lesson = Lesson.objects.create(title=self.title, description=self.description, video_link=self.video_link,
                                            course=self.course)

    def test_create_lesson(self):
        """Тест создания урока"""
        response = self.client.post(reverse('lms:lesson-create'),
                                    data={
                                        'title': self.title,
                                        'description': self.description,
                                        'video_link': self.video_link,
                                        'lesson': self.lesson.id,
                                        'course': self.course.id
                                    })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),
                         {'id': 2, 'title': 'Тестовый урок', 'owner': 1, 'description': 'Тестовое описание',
                          'video_link': 'https://www.youtube.com/', 'course': 1}
                         )
        self.assertEqual(Lesson.objects.count(), 2)

    def test_list_lesson(self):
        """Тест получения списка уроков"""
        response = self.client.get(reverse('lms:lesson-list'))
        self.assertEqual(response.status_code, 200)

    def test_update_lesson(self):
        """Тест обновления урока"""
        self.client.force_login(self.user)
        response = self.client.patch(reverse('lms:lesson-update', kwargs={'pk': self.lesson.id}), data={
            'title': 'Новый тестовый заголовок2',
        })
        self.assertEqual(response.status_code, 200)

    def test_delete_lesson(self):
        """Тест удаления урока"""
        self.client.force_login(self.user)
        response = self.client.delete(reverse('lms:lesson-delete', kwargs={'pk': self.lesson.id}))
        self.assertEqual(response.status_code, 204)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@mail.ru', password='123qwe456rty')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Тестовый курс', description='Тестовое описание')

    def test_subscription(self):
        """Тест подписки на курс"""
        response = self.client.post(reverse('lms:subs', args=[self.course.id]))
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(Subscription.objects.first().user, self.user)
        self.assertEqual(Subscription.objects.first().course, self.course)

    def test_unsubscription(self):
        """Тест отписки от курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(reverse('lms:subs', args=[self.course.id]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Subscription.objects.count(), 0)
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.paginators import CoursePaginator, LessonPaginator
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from lms.tasks import send_mail_about_update
from users.permissions import IsModerator, IsOwner


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]
        elif self.action in ['update']:
            self.permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     if self.action == 'list':
    #         if self.request.user.groups.filter(name="Модератор").exists():
    #             return self.queryset.all()
    #     if self.action == 'retrieve' and self.request.user.groups.filter(name="Модератор").exists():
    #         return self.queryset.all()
    #     return self.queryset.filter(owner=self.request.user)


class CreateLessonApiView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListLessonApiView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class DetailLessonApiView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class UpdateLessonApiView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    # permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]

    def perform_update(self, serializer):
        instance = serializer.save()
        subscriptions = Subscription.objects.filter(course=instance.course)
        for subscription in subscriptions:
            if self.request.user.id == subscription.user.id:
                send_mail_about_update.delay(course_name=instance.course.title)


class DeleteLessonApiView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]


class SubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated, ~IsModerator, IsOwner]
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_item = get_object_or_404(Course, id=kwargs.get('pk'))
        subs_item, created = Subscription.objects.get_or_create(user=user, course=course_item)
        if not created:
            subs_item.delete()
            message = 'Вы отписались от курса'
            status = HTTP_204_NO_CONTENT
        else:
            subs_item.save()
            message = 'Вы подписались на курс'
            status = HTTP_201_CREATED
        return Response({'message': message}, status=status)

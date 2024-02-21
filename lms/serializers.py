from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(max_length=255, validators=[LinkValidator])

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'owner', 'description', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'owner', 'description', 'lesson_count', 'lessons', 'subscription']

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lessons = instance.lesson_set.all()
        representation['lessons'] = LessonSerializer(lessons, many=True).data
        return representation

    def get_subscription(self, obj):
        user = self.context.get('request').user
        return Subscription.objects.filter(user=user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = [
            'id',
            'user',
            'course',
        ]

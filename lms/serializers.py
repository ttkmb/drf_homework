from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'owner', 'description', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'owner', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lessons = instance.lesson_set.all()
        representation['lessons'] = LessonSerializer(lessons, many=True).data
        return representation

from django.contrib.auth import get_user_model
from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_link', 'course']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.count', read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'lesson_count', 'lessons']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lessons = instance.lesson_set.all()
        representation['lessons'] = LessonSerializer(lessons, many=True).data
        return representation


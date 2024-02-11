from django.urls import path
from rest_framework import routers

from lms.apps import LmsConfig
from lms.views import CourseViewSet, CreateLessonApiView, ListLessonApiView, DetailLessonApiView, UpdateLessonApiView, \
    DeleteLessonApiView, UserUpdateAPIView

app_name = LmsConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/create/', CreateLessonApiView.as_view(), name='lesson-create'),
                  path('lesson/list/', ListLessonApiView.as_view(), name='lesson-list'),
                  path('lesson/detail/<int:pk>/', DetailLessonApiView.as_view(), name='lesson-detail'),
                  path('lesson/update/<int:pk>/', UpdateLessonApiView.as_view(), name='lesson-update'),
                  path('lesson/delete/<int:pk>/', DeleteLessonApiView.as_view(), name='lesson-delete'),
                  path('profile/<int:pk>/update/', UserUpdateAPIView.as_view(), name='profile-update'),
              ] + router.urls

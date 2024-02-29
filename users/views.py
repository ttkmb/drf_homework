from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from lms.models import Course
from users.models import Payments
from users.permissions import IsOwnerProfile
from users.serializers import UserSerializer, PaymentSerializer, ProductSerializer
from users.services import create_stripe_price, create_stripe_session, create_stripe_item


class UsersCreateView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()


class UsersListView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UsersDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UsersUpdateView(generics.UpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerProfile]


class UsersUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UsersDeleteView(generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticated]


class PaymentCourseCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        course_id = self.kwargs.get('pk')
        return get_object_or_404(Course, pk=course_id)

    def perform_create(self, serializer):
        payment = serializer.save()
        payment.owner = self.request.user
        course_item = self.get_object()
        product_name = create_stripe_item(course_item.title)
        stripe_price_id = create_stripe_price(payment.amount, product_name)
        payment.payment_link, payment.payment_id = create_stripe_session(stripe_price_id)
        payment.paid_course = course_item
        payment.save()


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['date']

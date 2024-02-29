from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import PaymentListView, UsersCreateView, UsersListView, UsersDetailView, \
    UsersDeleteView, UsersUpdateView, PaymentCourseCreateView, PaymentCreateView

app_name = UsersConfig.name


urlpatterns = [
    path('payments/course/<int:pk>/create/', PaymentCourseCreateView.as_view(), name='payments-course'),
    path('payments/create/', PaymentCreateView.as_view(), name='payments-create'),
    path('payments/', PaymentListView.as_view(), name='payments-list'),
    path('', UsersListView.as_view(), name='users-list'),
    path('register/', UsersCreateView.as_view(), name='users-register'),
    path('detail/<int:pk>/', UsersDetailView.as_view(), name='users-detail'),
    path('update/<int:pk>/', UsersUpdateView.as_view(), name='users-update'),
    path('delete/<int:pk>/', UsersDeleteView.as_view(), name='users-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
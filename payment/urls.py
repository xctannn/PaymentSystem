from django.urls import path
from .views import PaymentListView, PaymentDetailView, PaymentCreateView
from . import views

urlpatterns = [
    path('', PaymentListView.as_view(), name = 'payment-home'),
    path('new/', PaymentCreateView.as_view(), name = 'payment-create'),
    path('<pk>/', PaymentDetailView.as_view(), name = 'payment-detail'),
]
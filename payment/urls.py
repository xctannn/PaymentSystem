from django.urls import path
from .views import PaymentListView, PaymentDetailView, PaymentCreateView, VendorPaymentListView
from . import views

urlpatterns = [
    path('', PaymentListView.as_view(), name = 'payment-home'),
    path('vendor', VendorPaymentListView.as_view(), name = 'vendor-payment-home'),
    path('new/', PaymentCreateView.as_view(), name = 'payment-create'),
    path('<pk>/', PaymentDetailView.as_view(), name = 'payment-detail'),
    path('<pk>/edit/', views.UpdatePayment, name='payment-edit'),
    path('<pk>/verify', views.VerifyPayment, name = 'payment-verify'),
    path('<pk>/deny', views.DenyPayment, name = 'payment-deny'),
]
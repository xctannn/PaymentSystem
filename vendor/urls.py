from django.urls import path
from .views import VendorReceiptListView, VendorPaymentListView, VendorPaymentDetailView, VendorReceiptDetailView
from . import views

urlpatterns = [
    path('payment/', VendorPaymentListView.as_view(), name = 'vendor-payment-home'),
    path('receipt/', VendorReceiptListView.as_view(), name = 'vendor-receipt-home'),
    path('payment/<pk>', VendorPaymentDetailView.as_view(), name = 'vendor-payment-detail'),
    path('receipt/<pk>', VendorReceiptDetailView.as_view(), name = 'vendor-receipt-detail'),
    path('payment/<pk>/verify', views.VerifyPayment, name = 'vendor-payment-verify'),
    path('payment/<pk>/deny', views.DenyPayment, name = 'vendor-payment-deny'),
]
from django.urls import path
from .views import PaymentListView, ReceiptListView
from . import views
from payment.views import VerifyPayment, DenyPayment, PaymentDetailView
from receipt.views import RecieptDetailView

urlpatterns = [
    path('', PaymentListView.as_view(), name = 'vendor-home'),
    path('receipt/', ReceiptListView.as_view(), name = 'vendor-receipt'),
    path('<pk>/verify', VerifyPayment, name = 'payment-verify'),
    path('<pk>/deny', DenyPayment, name = 'payment-deny'),
]
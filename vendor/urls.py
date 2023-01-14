from django.urls import path
from .views import PaymentListView, ReceiptListView
from . import views
from payment.views import VerifyPayment, DenyPayment

urlpatterns = [
    #path('vendorlogin', LoginView.as_view(template_name='vendor/login.html'), name='login'),
    path('', PaymentListView.as_view(), name = 'vendor-home'),
    path('receipt/', ReceiptListView.as_view(), name = 'vendor-receipt'),
    path('<payment_id>/verify', VerifyPayment, name = 'vendor-verify'),
    path('<payment_id>/deny', DenyPayment, name = 'vendor-deny'),
]
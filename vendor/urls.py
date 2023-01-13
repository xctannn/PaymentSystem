from django.urls import path
from .views import PaymentListView, ReceiptListView

urlpatterns = [
    #path('vendorlogin', LoginView.as_view(template_name='vendor/login.html'), name='login'),
    path('', PaymentListView.as_view(), name = 'vendor-home'),
    path('receipt/', ReceiptListView.as_view(), name = 'vendor-receipt'),
]
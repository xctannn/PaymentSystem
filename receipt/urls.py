from django.urls import path
from .views import ReceiptListView, RecieptDetailView, ReceiptCreateView
from . import views

urlpatterns = [
    path('', ReceiptListView.as_view(), name = 'receipt-home'),
    path('new/', ReceiptCreateView.as_view(), name = 'receipt-create'),
    path('<pk>/', RecieptDetailView.as_view(), name = 'receipt-detail'),
    path('<pk>/edit/', views.UpdateReceipt, name='receipt-edit'),
]
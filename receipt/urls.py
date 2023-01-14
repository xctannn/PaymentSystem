from django.urls import path
from .views import ReceiptListView, ReceiptDetailView, ReceiptCreateView
from . import views

urlpatterns = [
    path('', ReceiptListView.as_view(), name = 'receipt-home'),
    path('new/', ReceiptCreateView.as_view(), name = 'receipt-create'),
    path('<pk>/', ReceiptDetailView.as_view(), name = 'receipt-detail'),
    path('<pk>/edit/', views.UpdateReceipt, name='receipt-edit'),
]
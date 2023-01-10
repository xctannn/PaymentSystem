from django.urls import path
from .views import ReceiptListView, RecieptDetailView, ReceiptCreateView, ReceiptEditListView, RecieptEditDetailView
from . import views

urlpatterns = [
    path('', ReceiptListView.as_view(), name = 'receipt-home'),
    path('new/', ReceiptCreateView.as_view(), name = 'receipt-create'),
    path('edit_requests/', ReceiptEditListView.as_view(), name = 'receipt-edit-home'),
    path('<pk>/', RecieptDetailView.as_view(), name = 'receipt-detail'),
    path('<pk>/edit/', views.UpdateReceipt, name='receipt-edit'),
    path('<pk>/requestDetail/',RecieptEditDetailView.as_view(), name='receipt-edit-detail'),
    path('<pk>/editRequest/', views.RequestReceiptEdit, name='receipt-edit-request'),
    path('<pk>/approve', views.ApproveRequestEdit, name='receipt-approve-edit'),
]
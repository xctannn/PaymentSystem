from django.urls import path
from .views import ReceiptListView, ReceiptDetailView, ReceiptCreateView, ReceiptEditListView, ReceiptEditDetailView
from . import views

urlpatterns = [
    path('', ReceiptListView.as_view(), name = 'receipt-home'),
    path('new/', ReceiptCreateView.as_view(), name = 'receipt-create'),
    path('edit_requests/', ReceiptEditListView.as_view(), name = 'receipt-edit-home'),
    path('<pk>/', ReceiptDetailView.as_view(), name = 'receipt-detail'),
    path('<pk>/edit/', views.UpdateReceipt, name='receipt-edit'),
    path('<pk>/editRequest/', views.RequestReceiptEdit, name='receipt-edit-request'),
    path('<pk>/requestDetail/',ReceiptEditDetailView.as_view(), name='receipt-edit-detail'),
    path('<pk>/requestDetail/approve', views.ApproveReceiptRequestEdit, name='receipt-approve-edit'),
    path('<pk>/requestDetail/deny', views.DenyReceiptRequestEdit, name='receipt-deny-edit'),
]
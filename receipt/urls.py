from django.urls import path
from .views import ReceiptListView, RecieptDetailView
# from . import views

urlpatterns = [
    path('', ReceiptListView.as_view(), name = 'receipt-home'),
    # path('new/', InvoiceCreateView.as_view(), name = 'invoice-create'),
    path('<pk>/', RecieptDetailView.as_view(), name = 'receipt-detail'),
    # path('<pk>/edit/', views.UpdateInvoice, name='invoice-edit'),
    # path('<pk>/edit/item/', views.UpdateItem, name='item-edit'),
]
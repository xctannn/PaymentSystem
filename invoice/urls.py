from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceCreateView, InvoiceEditListView, InvoiceEditDetailView
from . import views

urlpatterns = [
    path('', InvoiceListView.as_view(), name = 'invoice-home'),
    path('new/', InvoiceCreateView.as_view(), name = 'invoice-create'),
    path('edit_requests/', InvoiceEditListView.as_view(), name = 'invoice-edit-home'),
    path('<pk>/', InvoiceDetailView.as_view(), name = 'invoice-detail'),
    path('<pk>/edit/', views.UpdateInvoice, name='invoice-edit'),
    path('<pk>/edit/item/', views.UpdateItem, name='item-edit'),
    path('<pk>/requestEdit/', views.InvoiceEditRequest, name='invoice-edit-request'),
    path('<pk>/requestDetail/',InvoiceEditDetailView.as_view(), name='invoice-edit-detail'),
    path('<pk>/requestDetail/item/', views.ItemEditRequest, name='item-edit-request'),
    path('<pk>/requestDetail/approve', views.ApproveInvoiceRequestEdit, name='invoice-approve-edit'),
    path('<pk>/requestDetail/deny', views.DenyInvoiceRequestEdit, name='invoice-deny-edit'),
]
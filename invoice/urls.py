from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceCreateView
from . import views

urlpatterns = [
    path('', InvoiceListView.as_view(), name = 'invoice-home'),
    path('new/', InvoiceCreateView.as_view(), name = 'invoice-create'),
    path('<pk>/', InvoiceDetailView.as_view(), name = 'invoice-detail'),
    path('<pk>/edit/', views.UpdateInvoice, name='invoice-edit'),
    path('<pk>/edit/item/', views.UpdateItem, name='item-edit'),
]
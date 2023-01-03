from django.urls import path
from .views import InvoiceListView, InvoiceDetailView, InvoiceCreateView

urlpatterns = [
    path('', InvoiceListView.as_view(), name = 'invoice-home'),
    path('new/', InvoiceCreateView.as_view(), name = 'invoice-create'),
    path('<pk>/', InvoiceDetailView.as_view(), name = 'invoice-detail'),
]
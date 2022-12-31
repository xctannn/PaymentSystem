from django.urls import path
from .views import InvoiceListView, InvoiceDetailView

urlpatterns = [
    path('', InvoiceListView.as_view(), name = 'invoice-home'),
    path('<pk>/', InvoiceDetailView.as_view(), name = 'invoice-detail'),
]
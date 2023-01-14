from django.shortcuts import render
from receipt.models import Receipt
from payment.models import Payment
from django.views.generic import ListView

def home(request):
    return render(request, 'vendor/home.html')


class VendorPaymentListView(ListView):
    template_name = 'vendor/home.html'
    model= Payment
    context_object_name = 'payments'

class ReceiptListView(ListView):
    template_name = 'vendor/vendor_receipt.html'
    model= Receipt
    context_object_name = 'receipts'


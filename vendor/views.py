from django.shortcuts import render
from receipt.models import Receipt
from django.views.generic import ListView

def home(request):
    return render(request, 'vendor/home.html')


class PaymentListView(ListView):
    template_name = 'vendor/home.html'
    model= Receipt
    context_object_name = 'receipts'

class ReceiptListView(ListView):
    template_name = 'vendor/vendor_receipt.html'
    model= Receipt
    context_object_name = 'receipts'


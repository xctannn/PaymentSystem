from django.shortcuts import render
from .models import Receipt
from django.views.generic import ListView, DetailView

class ReceiptListView(ListView):
    model = Receipt
    template_name = 'receipt/home.html'
    context_object_name = 'receipts'
    ordering = ['-receipt_id']  #order by id

class RecieptDetailView(DetailView):
    model = Receipt
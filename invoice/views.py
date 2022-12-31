from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Invoice

def home(request):
    return render(request, 'invoice/home.html')

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice/home.html'
    context_object_name = 'invoices'
    ordering = ['-date']  #order by date

class InvoiceDetailView(DetailView):
    model = Invoice

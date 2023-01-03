from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from .models import Invoice, Item
from .forms import UploadInvoiceForm, AddItemForm

def home(request):
    return render(request, 'invoice/home.html')


class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice/home.html'
    context_object_name = 'invoices'
    ordering = ['-date']  #order by date


class InvoiceDetailView(DetailView):
    model = Invoice


class InvoiceCreateView(TemplateView):    
    template_name = 'invoice/invoice_form.html'

    def get(self, request):
        context = {
            'UploadInvoiceForm': UploadInvoiceForm(),
        }
        return render(request, self.template_name, context)
    

    def post(self, request):
        upload_invoice_form = UploadInvoiceForm(request.POST)
        add_item_form = AddItemForm(request.POST)
        
        if upload_invoice_form.is_valid():
            upload_invoice_form.save()
            context = {
                'AddItemForm': AddItemForm(),
            }
            return render(request, self.template_name, context)
            
        if request.method =='POST' and 'additem' in request.POST and add_item_form.is_valid():
            name = add_item_form.cleaned_data['name']
            unit_price = add_item_form.cleaned_data['unit_price']
            quantity = add_item_form.cleaned_data['quantity']
            total_price = add_item_form.cleaned_data['total_price']
            invoice_item = Invoice.objects.last()
            item = Item.objects.create(invoice = invoice_item, name = name, unit_price = unit_price, quantity = quantity, total_price = total_price)
            item.save()
            context = {
                'AddItemForm': AddItemForm(),
                'UploadButton': 'UploadButton',
            }
            return render(request, self.template_name, context)

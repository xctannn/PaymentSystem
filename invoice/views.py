from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, UpdateView
from .models import Invoice, Item
from .forms import UploadInvoiceForm, AddItemForm, UpdateInvoiceForm

class InvoiceListView(ListView):
    model = Invoice
    template_name = 'invoice/home.html'
    context_object_name = 'invoices'
    ordering = ['-date']  #order by date


class InvoiceDetailView(DetailView):
    model = Invoice


class InvoiceCreateView(TemplateView):    
    template_name = 'invoice/invoice_create_form.html'

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
            added_invoice = Invoice.objects.last()
            added_invoice.set_department()
            context = {
                'AddItemForm': AddItemForm(),
                'added_invoice': added_invoice,
            }
            return render(request, self.template_name, context)
            
        if request.method =='POST' and 'additem' in request.POST and add_item_form.is_valid():
            name = add_item_form.cleaned_data['name']
            unit_price = add_item_form.cleaned_data['unit_price']
            quantity = add_item_form.cleaned_data['quantity']
            total_price = add_item_form.cleaned_data['total_price']
            added_invoice = Invoice.objects.last()
            item = Item.objects.create(invoice = added_invoice, name = name, unit_price = unit_price, quantity = quantity, total_price = total_price)
            item.save()
            context = {
                'AddItemForm': AddItemForm(),
                'UploadButton': 'UploadButton',
                'added_invoice': added_invoice,
            }
            return render(request, self.template_name, context)


def UpdateInvoice(request, pk):                                         
    object = get_object_or_404(Invoice, pk=pk)
    form = UpdateInvoiceForm(instance=object)                                                               

    if request.method == "POST":
        form = UpdateInvoiceForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect ('item-edit', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    return render(request, 'invoice/invoice_update_form.html', context)


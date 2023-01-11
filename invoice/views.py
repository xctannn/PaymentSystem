from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Invoice, Item, InvoiceEdit, ItemEdit
from .forms import UploadInvoiceForm, AddItemForm, UpdateInvoiceForm, RequestInvoiceEditForm, RequestItemEditForm

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

x = 0
def getCount(object):
    global x
    x = (object.get_item_list()).count()
 

def UpdateInvoice(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    form = UpdateInvoiceForm(instance=object)
    getCount(object)

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


def UpdateItem(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    global x

    i = x - 1
    item = Item.objects.filter(invoice=object)[i]
    original_item_invoice = object
    original_item_name = item.name
    original_item_unit_price = item.unit_price
    original_item__quantity = item.quantity
    original_item_total_price = item.total_price
    initial_data = {'invoice': original_item_invoice, 'name': original_item_name, 'unit_price': original_item_unit_price, 'quantity': original_item__quantity, 'total_price': original_item_total_price}
    
    if request.method == "POST":
        form = AddItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            x -= 1
            if x == 0:
                return redirect ('invoice-detail', pk=pk)

            i = x - 1
            item = Item.objects.filter(invoice=object)[i]
            original_item = get_object_or_404(Item, pk=item.pk)
            original_item_invoice = object
            original_item_name = item.name
            original_item_unit_price = item.unit_price
            original_item__quantity = item.quantity
            original_item_total_price = item.total_price
            initial_data = {'invoice': original_item_invoice, 'name': original_item_name, 'unit_price': original_item_unit_price, 'quantity': original_item__quantity, 'total_price': original_item_total_price}
            
            form = AddItemForm(instance=item)
            context = {
                "form": form,
                "object": object,
            }
            return render(request, 'invoice/item_update_form.html', context)
    else:
        form = AddItemForm(instance=item)
        context = {
            "form": form,
            "object": object,
        }
        return render(request, 'invoice/item_update_form.html', context)

class InvoiceEditListView(ListView):
    model = InvoiceEdit
    template_name = 'invoice/invoice_edit_home.html'
    context_object_name = 'invoice_edits'
    ordering = ['-original_invoice_id'] 

class InvoiceEditDetailView(DetailView):
    model = InvoiceEdit
    template_name = 'invoice/invoice_edit_detail.html'

def InvoiceEditRequest(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    original_due_date = object.due_date
    original_vendor = object.vendor
    original_amount_charged = object.amount_charged
    original_tax = object.tax
    original_amount_owed = object.amount_owed
    intial_data = {'original_invoice_id': object, 'due_date': original_due_date, 'vendor': original_vendor, 'amount_charged': original_amount_charged, 'tax': original_tax, 'amount_owed': original_amount_owed} # 'editor': request.user
    form = RequestInvoiceEditForm(initial=intial_data)
    getCount(object)

    if request.method == "POST":
        form = RequestInvoiceEditForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('item-edit-request', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    return render(request, 'invoice/invoice_edit_request_form.html', context)


def ItemEditRequest(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    global x

    i = x - 1
    item = Item.objects.filter(invoice=object)[i]
    original_item = get_object_or_404(Item, pk=item.pk)
    original_item_invoice = object
    item_invoice_edit = InvoiceEdit.objects.all().last()
    original_item_name = item.name
    original_item_unit_price = item.unit_price
    original_item__quantity = item.quantity
    original_item_total_price = item.total_price
    initial_data = {'original_item_id': original_item, 'invoice': original_item_invoice, 'invoice_edit': item_invoice_edit, 'name': original_item_name, 'unit_price': original_item_unit_price, 'quantity': original_item__quantity, 'total_price': original_item_total_price}
    
    if request.method == "POST":
        form = RequestItemEditForm(request.POST)
        if form.is_valid():
            form.save()
            x -= 1
            if x == 0:
                return redirect ('invoice-detail', pk=pk)

            i = x - 1
            item = Item.objects.filter(invoice=object)[i]
            original_item = get_object_or_404(Item, pk=item.pk)
            original_item_invoice = object
            item_invoice_edit = InvoiceEdit.objects.all().last()
            original_item_name = item.name
            original_item_unit_price = item.unit_price
            original_item__quantity = item.quantity
            original_item_total_price = item.total_price
            initial_data = {'original_item_id': original_item, 'invoice': original_item_invoice, 'invoice_edit': item_invoice_edit, 'name': original_item_name, 'unit_price': original_item_unit_price, 'quantity': original_item__quantity, 'total_price': original_item_total_price}
            
            form = RequestItemEditForm(initial=initial_data)
            context = {
                "form": form,
                "object": object,
            }
            return render(request, 'invoice/item_edit_request_form.html', context)
    else:
        form = RequestItemEditForm(initial=initial_data)
        context = {
            "form": form,
            "object": object,
        }
        return render(request, 'invoice/item_edit_request_form.html', context)
    
def ApproveInvoiceRequestEdit(request, pk):
    object = get_object_or_404(InvoiceEdit, pk=pk)

    object.editOriginalInvoice()
    item_edit_requests = ItemEdit.objects.filter(invoice_edit = object.pk)

    for item in item_edit_requests:
        item.editOriginalItem()
        item.delete()
    object.delete()

    return redirect('invoice-edit-home')

def DenyInvoiceRequestEdit(request, pk):
    object = InvoiceEdit.objects.get(pk=pk)
    item_edit_requests = ItemEdit.objects.filter(invoice_edit = object.pk)

    for item in item_edit_requests:
        item.delete()  
    object.delete()

    return redirect('invoice-edit-home')
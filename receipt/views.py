from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt, ReceiptEdit
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadReceiptForm, RequestReceiptEditForm

class ReceiptListView(ListView):
    model = Receipt
    template_name = 'receipt/home.html'
    context_object_name = 'receipts'
    ordering = ['-receipt_id']  #order by id


class RecieptDetailView(DetailView):
    model = Receipt


class ReceiptCreateView(TemplateView):    
    template_name = 'receipt/receipt_create_form.html'
    
    def get(self, request):
        context = {
            'UploadReceiptForm': UploadReceiptForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        upload_receipt_form = UploadReceiptForm(request.POST)
        if upload_receipt_form.is_valid():
            upload_receipt_form.save()
            return redirect('receipt-home')


def UpdateReceipt(request, pk):
    object = get_object_or_404(Receipt, pk=pk)
    form = UploadReceiptForm(instance=object)

    if request.method == "POST":
        form = UploadReceiptForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect ('receipt-detail', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    return render(request, 'receipt/receipt_update_form.html', context)


class ReceiptEditListView(ListView):
    model = ReceiptEdit
    template_name = 'receipt/receipt_edit_home.html'
    context_object_name = 'receiptEdits'
    ordering = ['-original_receipt_id']  #order by original receipt id

class RecieptEditDetailView(DetailView):
    model = ReceiptEdit

def RequestReceiptEdit(request, pk):
    object = get_object_or_404(Receipt, pk=pk)

    original_date = object.date
    original_invoice = object.invoice
    original_vendor = object.vendor
    # current_user = request.user

    initial_data = {'date': original_date,'original_receipt_id': object, 'invoice': original_invoice, 'vendor': original_vendor} # 'editor': current_user
    form = RequestReceiptEditForm(initial=initial_data)

    if request.method == "POST":
        form = RequestReceiptEditForm(request.POST, initial=initial_data)
        if form.is_valid():
            form.save()

            # new_receipt_edit = ReceiptEdit.objects.last()
            # new_receipt_edit.set_editor(current_user)

            # new_receipt_edit.set_original_receipt_id(original_invoice)

            return redirect ('receipt-detail', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    return render(request, 'receipt/receipt_edit_request_form.html', context)

def ApproveRequestEdit(request, pk):
    object = get_object_or_404(ReceiptEdit, pk=pk)

    object.editOriginalReceipt()
    object.delete()

    return redirect('receipt-edit-home')

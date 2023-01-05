from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadReceiptForm

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

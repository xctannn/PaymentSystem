from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt, ReceiptEdit
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadReceiptForm, UpdateReceiptForm, RequestReceiptEditForm
from account.models import EmployeeProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def is_CFO(User):
    return User.groups.filter(name='CFO').exists()

def is_FO(User):
    return User.groups.filter(name='Finance Officer').exists()

class ReceiptListView(LoginRequiredMixin, ListView):
    model = Receipt
    template_name = 'receipt/home.html'
    context_object_name = 'receipts'
    ordering = ['-receipt_id']  #order by id

    def get_queryset(self):
        self.employee = get_object_or_404(EmployeeProfile, user=self.request.user)
        if is_CFO(self.request.user):
            return Receipt.objects.all()
        elif is_FO(self.request.user):
            return Receipt.objects.filter(department=self.employee.department)
    
    def get_context_data(self, **kwargs):
        context = super(ReceiptListView, self).get_context_data(**kwargs)
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
        return context


class ReceiptDetailView(LoginRequiredMixin, DetailView):
    model = Receipt
    def get_context_data(self, **kwargs):
        context = super(ReceiptDetailView, self).get_context_data(**kwargs)
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
        if is_FO(self.request.user):
            context['FO'] = "FO"
        return context


class ReceiptCreateView(LoginRequiredMixin, TemplateView):    
    template_name = 'receipt/receipt_create_form.html'
    
    def get(self, request):
        context = {
            'UploadReceiptForm': UploadReceiptForm(),
        }
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
        return render(request, self.template_name, context)
    
    def post(self, request):
        upload_receipt_form = UploadReceiptForm(request.POST)
        if upload_receipt_form.is_valid():
            upload_receipt_form.save()
            added_receipt = Receipt.objects.latest('added_date')
            employee = EmployeeProfile.objects.get(user = self.request.user)
            added_receipt.set_uploader(employee)
            added_receipt.set_department()
            return redirect('receipt-home')

@login_required
def UpdateReceipt(request, pk):
    object = get_object_or_404(Receipt, pk=pk)
    form = UpdateReceiptForm(instance=object)

    if request.method == "POST":
        form = UpdateReceiptForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect ('receipt-detail', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    if is_CFO(request.user):
        context['CFO'] = "CFO"
    return render(request, 'receipt/receipt_update_form.html', context)


class ReceiptEditListView(LoginRequiredMixin, ListView):
    model = ReceiptEdit
    template_name = 'receipt/receipt_edit_home.html'
    context_object_name = 'receipt_edits'
    ordering = ['-original_receipt_id']  #order by original receipt id
    def get_context_data(self, **kwargs):
        context = super(ReceiptEditListView, self).get_context_data(**kwargs)
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
        return context 

class RecieptEditDetailView(LoginRequiredMixin, DetailView):
    model = ReceiptEdit
    template_name = 'receipt/receipt_edit_detail.html'
    def get_context_data(self, **kwargs):
        context = super(RecieptEditDetailView, self).get_context_data(**kwargs)
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
        return context  

@login_required
def RequestReceiptEdit(request, pk):
    object = get_object_or_404(Receipt, pk=pk)

    original_date = object.date
    original_invoice = object.invoice
    original_vendor = object.vendor
    initial_data = {'date': original_date,'original_receipt_id': object, 'invoice': original_invoice, 'vendor': original_vendor}
    form = RequestReceiptEditForm(initial=initial_data)

    if request.method == "POST":
        form = RequestReceiptEditForm(request.POST, initial=initial_data)
        if form.is_valid():
            form.save()
            new_receipt_edit_request = ReceiptEdit.objects.latest('added_date')
            editor = EmployeeProfile.objects.get(user = request.user)
            new_receipt_edit_request.set_editor(editor)
            new_receipt_edit_request.send_request_notification()
            return redirect ('receipt-detail', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    return render(request, 'receipt/receipt_edit_request_form.html', context)

def ApproveReceiptRequestEdit(request, pk):
    object = get_object_or_404(ReceiptEdit, pk=pk)

    object.edit_original_receipt()
    object.send_request_approval_notification()
    object.delete()

    return redirect('receipt-edit-home')

def DenyReceiptRequestEdit(request, pk):
    object = get_object_or_404(ReceiptEdit, pk=pk)
    object.send_request_deny_notification()
    object.delete()

    return redirect('receipt-edit-home')
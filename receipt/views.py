from django.shortcuts import render, redirect, get_object_or_404
from .models import Receipt
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadReceiptForm
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
            added_receipt = Receipt.objects.last()
            employee = EmployeeProfile.objects.get(user = self.request.user)
            added_receipt.set_uploader(employee)
            added_receipt.set_department()
            return redirect('receipt-home')

@login_required
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
    if is_CFO(request.user):
        context['CFO'] = "CFO"
    return render(request, 'receipt/receipt_update_form.html', context)

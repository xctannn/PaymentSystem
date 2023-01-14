from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadPaymentForm 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from account.models import EmployeeProfile

def is_CFO(User):
    return User.groups.filter(name='CFO').exists()

class VendorPaymentListView(ListView):
    template_name = 'payment/vendor_payment.html'
    model= Payment
    context_object_name = 'payments'

class PaymentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Payment
    template_name = 'payment/home.html'
    context_object_name =  'payments'
    ordering = ['-payment_id']  #order by id
    extra_context={"CFO": "CFO"}

    def test_func(self):
        return is_CFO(self.request.user)


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    extra_context={"CFO": "CFO"}


class PaymentCreateView(LoginRequiredMixin, TemplateView):    
    template_name =  'payment/payment_create_form.html'
    
    def get(self, request):
        context = {
            'UploadPaymentForm': UploadPaymentForm(),
            'CFO' : "CFO",
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        upload_payment_form = UploadPaymentForm(request.POST)
        if upload_payment_form.is_valid():
            upload_payment_form.save()
            added_payment = Payment.objects.last()
            employee = EmployeeProfile.objects.get(user = self.request.user)
            added_payment.set_uploader(employee)
            return redirect('payment-home')

@login_required
def UpdatePayment(request, pk):
    object = get_object_or_404 (Payment, pk=pk)
    form = UploadPaymentForm(instance=object)

    if request.method == "POST":
        form = UploadPaymentForm(request.POST, instance=object)
        if form.is_valid():
            form.save()
            return redirect ('payment-detail', pk=pk)

    context = {
        "form": form,
        "object": object,
        'CFO' : "CFO",
    }
    return render(request,  'payment/payment_update_form.html', context)


@login_required
def VerifyPayment(request, pk):
    object = get_object_or_404(Payment, pk=pk)
    object.verify()

    return redirect('invoice-home')


@login_required
def DenyPayment(request, pk):
    object = Payment.objects.get(pk=pk)
    object.deny()

    return redirect('invoice-home')
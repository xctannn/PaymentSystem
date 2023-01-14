from django.shortcuts import get_object_or_404, redirect
from receipt.models import Receipt
from payment.models import Payment
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from account.models import VendorProfile

def is_vendor(User):
    return User.groups.filter(name='Vendor').exists()

class VendorPaymentListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'vendor/vendor_payment.html'
    model= Payment
    context_object_name = 'payments'

    def test_func(self):
        return is_vendor(self.request.user)

    def get_queryset(self):
        self.vendor = get_object_or_404(VendorProfile, user=self.request.user)
        return Payment.objects.filter(vendor=self.vendor)


class VendorReceiptListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'vendor/vendor_receipt.html'
    model= Receipt
    context_object_name = 'receipts'

    def test_func(self):
        return is_vendor(self.request.user)

    def get_queryset(self):
        self.vendor = get_object_or_404(VendorProfile, user=self.request.user)
        return Receipt.objects.filter(vendor=self.vendor)


class VendorPaymentDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Payment
    template_name =  'vendor/payment_detail.html'

    def test_func(self):
        return is_vendor(self.request.user)


class VendorReceiptDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Receipt
    template_name =  'vendor/receipt_detail.html'

    def test_func(self):
        return is_vendor(self.request.user)

@login_required
def VerifyPayment(request, pk):
    object = get_object_or_404(Payment, pk=pk)
    object.verify()

    return redirect('vendor-payment-home')


@login_required
def DenyPayment(request, pk):
    object = Payment.objects.get(pk=pk)
    object.deny()

    return redirect('vendor-payment-home')

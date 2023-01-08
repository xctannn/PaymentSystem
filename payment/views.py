from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadPaymentForm 

class PaymentListView(ListView):
    model = Payment
    template_name = 'payment/home.html'
    context_object_name =  'payments'
    ordering = ['payment_id']  #order by id


class PaymentDetailView(DetailView):
    model = Payment


class PaymentCreateView(TemplateView):    
    template_name =  'payment/payment_create_form.html'
    
    def get(self, request):
        context = {
            'UploadPaymentForm': UploadPaymentForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        upload_payment_form = UploadPaymentForm(request.POST)
        if upload_payment_form.is_valid():
            upload_payment_form.save()
            return redirect('payment-home')


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
    }
    return render(request,  'payment/payment_update_form.html', context)

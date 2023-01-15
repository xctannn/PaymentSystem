from django.shortcuts import render, redirect, get_object_or_404
from .models import Payment
from django.views.generic import ListView, DetailView, TemplateView
from .forms import UploadPaymentForm 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from account.models import EmployeeProfile

def is_CFO(User):
    return User.groups.filter(name='CFO').exists()

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
            added_payment = Payment.objects.latest('added_date')
            employee = EmployeeProfile.objects.get(user = self.request.user)
            added_payment.set_uploader(employee)
            added_payment.send_verification_request()
            return redirect('payment-home')

        else:
            context = {
                'msg': "Invalid data keyed in.",
                'UploadPaymentForm': UploadPaymentForm(),
                'CFO' : "CFO",
            }
            return render(request, self.template_name, context)

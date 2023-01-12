from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Invoice, Item
from .forms import FOUploadInvoiceForm, CFOUploadInvoiceForm, AddItemForm, UpdateInvoiceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from account.models import EmployeeProfile

def is_CFO(User):
    return User.groups.filter(name='CFO').exists()

def is_FO(User):
    return User.groups.filter(name='Finance Officer').exists()
    
class InvoiceListView(LoginRequiredMixin, ListView):
    template_name = 'invoice/home.html'
    context_object_name = 'invoices'
    ordering = ['-date']  #order by date

    def get_queryset(self):
        self.employee = get_object_or_404(EmployeeProfile, user=self.request.user)
        if is_CFO(self.request.user):
            return Invoice.objects.all()
        elif is_FO(self.request.user):
            return Invoice.objects.filter(department=self.employee.department)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(InvoiceListView, self).get_context_data(**kwargs)
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
        return context


class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    
    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        if is_CFO(self.request.user):
            self.CFO = get_object_or_404(EmployeeProfile, user=self.request.user)
            if (self.CFO == EmployeeProfile.objects.filter(position='CFO').first()):
                context['CFO1'] = "CFO1"
            else:
                context['CFO2'] = "CFO2"
        return context


class InvoiceCreateView(LoginRequiredMixin, TemplateView):    
    template_name = 'invoice/invoice_create_form.html'

    def get(self, request):
        context = {}
        if is_CFO(self.request.user):
            context['CFO'] = "CFO"
            context['UploadInvoiceForm'] = CFOUploadInvoiceForm()
        if is_FO(self.request.user):
            context['UploadInvoiceForm'] = FOUploadInvoiceForm()
        return render(request, self.template_name, context)
    

    def post(self, request):
        CFO_upload_invoice_form = CFOUploadInvoiceForm(request.POST)
        FO_upload_invoice_form = FOUploadInvoiceForm(request.POST)
        add_item_form = AddItemForm(request.POST)
        
        if CFO_upload_invoice_form.is_valid():
            CFO_upload_invoice_form.save()
            added_invoice = Invoice.objects.last()
            employee = EmployeeProfile.objects.get(user = self.request.user)
            added_invoice.set_uploader(employee)
            context['CFO'] = "CFO"
            context = {
                'AddItemForm': AddItemForm(),
                'added_invoice': added_invoice,
            }
            return render(request, self.template_name, context)

        if FO_upload_invoice_form.is_valid():
            FO_upload_invoice_form.save()
            added_invoice = Invoice.objects.last()
            employee = EmployeeProfile.objects.get(user = self.request.user)
            added_invoice.set_uploader(employee)
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
            if is_CFO(self.request.user):
                context['CFO'] = "CFO"
            context = {
                'AddItemForm': AddItemForm(),
                'UploadButton': 'UploadButton',
                'added_invoice': added_invoice,
            }
            return render(request, self.template_name, context)

        else:
            context = {
                'msg': "Invoice ID duplicate.",
            }
            return render(request, self.template_name, context)

x = 0
def getCount(object):
    global x
    x = (object.get_item_list()).count()

@login_required
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
    if is_CFO(request.user):
        context['CFO'] = "CFO"
    return render(request, 'invoice/invoice_update_form.html', context)

@login_required
def UpdateItem(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    global x

    if request.method == "POST":
        item_object = Item.objects.get(pk = x)
        item_object.name = ""
        item_object.unit_price = ""
        item_object.quantity = ""
        item_object.total_price = ""
        
        form = AddItemForm(request.POST, instance=item_object)
        x -= 1
        if form.is_valid():
            form.save()
            form = AddItemForm()
        context = {
            "form": form,
            "object": object,
        }
        if is_CFO(request.user):
            context['CFO'] = "CFO"
        if x <= 0:
            return redirect ('invoice-detail', pk=pk)
        return render(request, 'invoice/item_update_form.html', context)

    else:
        item_object = Item.objects.get(pk = x)
        item_object.name = ""
        item_object.unit_price = ""
        item_object.quantity = ""
        item_object.total_price = ""

        form = AddItemForm(instance=item_object)
        context = {
            "form": form,
            "object": object,
        }
        if is_CFO(request.user):
            context['CFO'] = "CFO"
        return render(request, 'invoice/item_update_form.html', context)


@login_required
def ApprovePayment(request, pk):
    invoice = Invoice.objects.get(pk=pk)
    if invoice.first_CFO_approved == False:
        invoice.set_first_CFO_approve()
    else:
        invoice.set_second_CFO_approve()
        invoice.set_approved_date()
    return redirect('invoice-detail', pk=pk)
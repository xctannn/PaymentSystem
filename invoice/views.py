from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Invoice, Item, InvoiceEdit, ItemEdit
from .forms import FOUploadInvoiceForm, CFOUploadInvoiceForm, AddItemForm, UpdateInvoiceForm, RequestInvoiceEditForm, RequestItemEditForm
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
        if is_FO(self.request.user):
            context['FO'] = "FO"
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

        if is_CFO(self.request.user):
            if CFO_upload_invoice_form.is_valid():
                CFO_upload_invoice_form.save()
                added_invoice = Invoice.objects.latest('added_date')
                employee = EmployeeProfile.objects.get(user = self.request.user)
                added_invoice.set_uploader(employee)
                added_invoice.send_invoice_payment_request_notification_to_all_CFO()
                context = {
                    'AddItemForm': AddItemForm(),
                    'added_invoice': added_invoice,
                }
                context['CFO'] = "CFO"
                return render(request, self.template_name, context)

        if is_FO(self.request.user):
            if FO_upload_invoice_form.is_valid():
                FO_upload_invoice_form.save()
                added_invoice = Invoice.objects.latest('added_date')
                employee = EmployeeProfile.objects.get(user = self.request.user)
                added_invoice.set_uploader(employee)
                added_invoice.set_department()
                added_invoice.send_invoice_payment_request_notification_to_all_CFO()
                context = {
                    'AddItemForm': AddItemForm(),
                    'added_invoice': added_invoice,
                }
                return render(request, self.template_name, context)

        if add_item_form.is_valid():
            name = add_item_form.cleaned_data['name']
            unit_price = add_item_form.cleaned_data['unit_price']
            quantity = add_item_form.cleaned_data['quantity']
            total_price = add_item_form.cleaned_data['total_price']
            added_invoice = Invoice.objects.latest('added_date')
            item = Item.objects.create(invoice = added_invoice, name = name, unit_price = unit_price, quantity = quantity, total_price = total_price)
            item.save() 
            context = {
                'AddItemForm': AddItemForm(),
                'UploadButton': 'UploadButton',
                'added_invoice': added_invoice,
            }
            if is_CFO(self.request.user):
                context['CFO'] = "CFO"
            return render(request, self.template_name, context)

        else:
            context = {
                'msg': "Invalid data keyed in.",
            }
            if is_CFO(self.request.user):
                context['CFO'] = "CFO"
                context['UploadInvoiceForm'] = CFOUploadInvoiceForm()
            if is_FO(self.request.user):
                context['UploadInvoiceForm'] = FOUploadInvoiceForm()
            return render(request, self.template_name, context)

item_count = 0
def getCount(object):
    global item_count
    item_count = (object.get_item_list()).count()

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
    global item_count

    i = item_count - 1
    item = Item.objects.filter(invoice=object)[i]
   
    if request.method == "POST":
        form = AddItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            item_count -= 1
            if item_count == 0:
                return redirect ('invoice-detail', pk=pk)

            i = item_count - 1
            item = Item.objects.filter(invoice=object)[i]
            
            form = AddItemForm(instance=item)
            context = {
                "form": form,
                "object": object,
            }
            if is_CFO(request.user):
                context['CFO'] = "CFO"
            return render(request, 'invoice/item_update_form.html', context)
            
    else:
        form = AddItemForm(instance=item)
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
    if is_CFO(request.user):
        CFO = get_object_or_404(EmployeeProfile, user=request.user)
        if CFO == EmployeeProfile.objects.filter(position='CFO').first():
            invoice.set_first_CFO_approve()
            invoice.send_invoice_payment_request_notification_to_other_CFO(CFO)
        elif CFO == EmployeeProfile.objects.filter(position='CFO').last():
            invoice.set_second_CFO_approve()
            invoice.send_invoice_payment_request_notification_to_other_CFO(CFO)
    if invoice.first_CFO_approved == True and invoice.second_CFO_approved == True:
        invoice.set_approved_date()
        invoice.send_invoice_payment_approval_notification()
    return redirect('invoice-detail', pk=pk)


class InvoiceEditListView(LoginRequiredMixin, ListView):
    model = InvoiceEdit
    template_name = 'invoice/invoice_edit_home.html'
    context_object_name = 'invoice_edits'
    ordering = ['-original_invoice_id']
    extra_context={"CFO": "CFO"}

class InvoiceEditDetailView(LoginRequiredMixin, DetailView):
    model = InvoiceEdit
    template_name = 'invoice/invoice_edit_detail.html'  
    extra_context={"CFO": "CFO"}

@login_required
def InvoiceEditRequest(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    original_date = object.date
    original_due_date = object.due_date
    original_vendor = object.vendor
    original_amount_charged = object.amount_charged
    original_tax = object.tax
    original_amount_owed = object.amount_owed
    intial_data = {'original_invoice_id': object, 'date': original_date, 'due_date': original_due_date, 'vendor': original_vendor, 'amount_charged': original_amount_charged, 'tax': original_tax, 'amount_owed': original_amount_owed}
    form = RequestInvoiceEditForm(initial=intial_data)
    getCount(object)

    if request.method == "POST":
        form = RequestInvoiceEditForm(request.POST)
        if form.is_valid():
            form.save()
            added_invoice_edit = InvoiceEdit.objects.latest('added_date')
            editor = EmployeeProfile.objects.get(user = request.user)
            added_invoice_edit.set_editor(editor)
            return redirect ('item-edit-request', pk=pk)

    context = {
        "form": form,
        "object": object,
    }
    return render(request, 'invoice/invoice_edit_request_form.html', context)


@login_required
def ItemEditRequest(request, pk):
    object = get_object_or_404(Invoice, pk=pk)
    global item_count

    i = item_count - 1
    item = Item.objects.filter(invoice=object)[i]
    original_item = get_object_or_404(Item, pk=item.pk)
    original_item_invoice = object
    item_invoice_edit = InvoiceEdit.objects.latest('added_date')
    original_item_name = item.name
    original_item_unit_price = item.unit_price
    original_item__quantity = item.quantity
    original_item_total_price = item.total_price
    initial_data = {'original_item_id': original_item, 'invoice': original_item_invoice, 'invoice_edit': item_invoice_edit, 'name': original_item_name, 'unit_price': original_item_unit_price, 'quantity': original_item__quantity, 'total_price': original_item_total_price}
    
    if request.method == "POST":
        form = RequestItemEditForm(request.POST)
        if form.is_valid():
            form.save()
            item_count -= 1
            if item_count == 0:
                new_invoice_edit_request = InvoiceEdit.objects.latest('added_date')
                new_invoice_edit_request.send_request_notification()
                return redirect ('invoice-detail', pk=pk)

            i = item_count - 1
            item = Item.objects.filter(invoice=object)[i]
            original_item = get_object_or_404(Item, pk=item.pk)
            original_item_invoice = object
            item_invoice_edit = InvoiceEdit.objects.latest('added_date')
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


@login_required
def ApproveInvoiceRequestEdit(request, pk):
    object = get_object_or_404(InvoiceEdit, pk=pk)

    object.edit_original_invoice()
    item_edit_requests = ItemEdit.objects.filter(invoice_edit = object.pk)

    for item in item_edit_requests:
        item.edit_original_item()
        item.delete()

    object.send_request_approval_notification()
    object.delete()

    return redirect('invoice-edit-home')


@login_required
def DenyInvoiceRequestEdit(request, pk):
    object = InvoiceEdit.objects.get(pk=pk)
    item_edit_requests = ItemEdit.objects.filter(invoice_edit = object.pk)

    for item in item_edit_requests:
        item.delete()  

    object.send_request_deny_notification()
    object.delete()

    return redirect('invoice-edit-home')

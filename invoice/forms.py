from django import forms
from .models import Invoice, Item, InvoiceEdit, ItemEdit

class FOUploadInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
    
        fields = [
            'invoice_id',
            'date',
            'due_date',
            'vendor',
            'amount_charged',
            'tax',
            'amount_owed',
        ]

        labels = {
            'invoice_id': 'Invoice ID ',
            'date': "Date ",
            'due_date': 'Due Date ',
            'vendor': 'Vendor ',
            'amount_charged': 'Subtotal ',
            'tax': 'Tax (%) ',
            'amount_owed': 'Amount Owed ',
        }

        widgets = { 
            'invoice_id' : forms.TextInput(attrs={'class' : 'form-control'}),
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'due_date' : forms.NumberInput(attrs={'type': 'date'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
            'amount_charged' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'tax' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'amount_owed' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
        }

class CFOUploadInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
    
        fields = [
            'invoice_id',
            'date',
            'due_date',
            'vendor',
            'amount_charged',
            'tax',
            'amount_owed',
            'department',
        ]

        labels = {
            'invoice_id': 'Invoice ID ',
            'date': "Date ",
            'due_date': 'Due Date ',
            'vendor': 'Vendor ',
            'amount_charged': 'Subtotal ',
            'tax': 'Tax (%) ',
            'amount_owed': 'Amount Owed ',
        }

        widgets = { 
            'invoice_id' : forms.TextInput(attrs={'class' : 'form-control'}),
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'due_date' : forms.NumberInput(attrs={'type': 'date'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
            'amount_charged' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'tax' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'amount_owed' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'department' : forms.Select(attrs={'class' : 'form-control'}),
        }


class AddItemForm(forms.ModelForm):
    
    class Meta:
        model = Item

        fields = [
            'invoice',
            'name',
            'unit_price',
            'quantity',
            'total_price',
        ]

        labels = {
            'name': 'Item',
            'unit_price': "Unit Price ",
            'quantity': 'Quantity ',
            'total_price': 'Total Price ',
        }

        widgets = { 
            'invoice' : forms.HiddenInput,
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'unit_price' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'quantity' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'total_price' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
        }


class UpdateInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
    
        fields = [
            'date',
            'due_date',
            'vendor',
            'amount_charged',
            'tax',
            'amount_owed',
        ]

        labels = {
            'date': "Date ",
            'due_date': 'Due Date ',
            'vendor': 'Vendor ',
            'amount_charged': 'Subtotal ',
            'tax': 'Tax (%) ',
            'amount_owed': 'Amount Owed ',
        }

        widgets = { 
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'due_date' : forms.NumberInput(attrs={'type': 'date'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
            'amount_charged' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'tax' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'amount_owed' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
        }

class RequestInvoiceEditForm(forms.ModelForm):

    class Meta:
        model = InvoiceEdit
    
        fields = [
            'original_invoice_id',
            'due_date',
            'vendor',
            'amount_charged',
            'tax',
            'amount_owed',
            'editor',
        ]

        labels = {
            'original_invoice_id': 'Original Invoice ID',
            'due_date': 'Due Date ',
            'vendor': 'Vendor ',
            'amount_charged': 'Subtotal ',
            'tax': 'Tax (%) ',
            'amount_owed': 'Amount Owed ',
        }

        widgets = { 
            'original_invoice_id': forms.HiddenInput,
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'due_date' : forms.NumberInput(attrs={'type': 'date'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
            'amount_charged' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'tax' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'amount_owed' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'uploader' : forms.Select(attrs={'class' : 'form-control'}),
        }

class RequestItemEditForm(forms.ModelForm):
    
    class Meta:
        model = ItemEdit

        fields = [
            'original_item_id',
            'invoice',
            'invoice_edit',
            'name',
            'unit_price',
            'quantity',
            'total_price',
        ]

        labels = {
            'original_item_id': "original Item",
            'invoice': "Invoice",
            'name': 'Item',
            'unit_price': "Unit Price ",
            'quantity': 'Quantity ',
            'total_price': 'Total Price ',
        }

        widgets = { 
            'original_item_id' : forms.HiddenInput,
            'invoice' : forms.HiddenInput,
            'invoice_edit': forms.HiddenInput,
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'unit_price' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'quantity' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'total_price' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
        }
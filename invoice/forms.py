from django import forms
from .models import Invoice, Item

class UploadInvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
    
        fields = [
            'invoice_id',
            'date',
            'due_date',
            'vendor',
            'amount_charged',
            'tax',
            'amount_owned',
            'uploader',
        ]

        # Styling form
        labels = {
            'invoice_id': 'Invoice ID ',
            'date': "Date ",
            'due_date': 'Due Date ',
            'vendor': 'Vendor ',
            'amount_charged': 'Subtotal ',
            'tax': 'Tax (%) ',
            'amount_owned': 'Amount Owned ',
        }

        widgets = { 
            'invoice_id' : forms.TextInput(attrs={'class' : 'form-control'}),
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'due_date' : forms.NumberInput(attrs={'type': 'date'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
            'amount_charged' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'tax' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'amount_owned' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'uploader' : forms.Select(attrs={'class' : 'form-control'}),
        }

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item

        fields = [
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
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'unit_price' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'quantity' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
            'total_price' : forms.NumberInput(attrs={'class' : 'form-control', 'min': 0,}),
        }
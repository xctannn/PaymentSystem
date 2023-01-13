from django import forms
from .models import Receipt, ReceiptEdit

class UploadReceiptForm(forms.ModelForm):
    
    class Meta:
        model = Receipt
        
        fields = [
            'receipt_id',
            'date',
            'invoice',
            'vendor',
        ]

        labels = {
            'receipt_id': 'Receipt ID ',
            'date': "Date ",
            'invoice': 'Invoice ID ',
            'vendor': 'Vendor ',
        }

        widgets = { 
            'receipt_id' : forms.TextInput(attrs={'class' : 'form-control'}),
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'invoice' : forms.Select(attrs={'class' : 'form-control'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
        }

class RequestReceiptEditForm(forms.ModelForm):
    
    class Meta:
        model = ReceiptEdit
        
        fields = [
            'original_receipt_id',
            'date',
            'invoice',
            'vendor',
            'editor'
        ]

        labels = {
            'original_receipt_id': 'Receipt ID ',
            'date': "Date ",
            'invoice': 'Invoice ID ',
            'vendor': 'Vendor ',
            'editor': 'Editor ',
        }

        widgets = { 
            'original_receipt_id' : forms.HiddenInput,
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'invoice' : forms.Select(attrs={'class' : 'form-control'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
            'editor' : forms.Select(attrs={'class' : 'form-control'}),
        }
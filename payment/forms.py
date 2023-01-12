from django import forms
from .models import Payment

class UploadPaymentForm(forms.ModelForm):
    
    class Meta:
        model = Payment
        
        fields = [
            'payment_id',
            'date',
            'invoice',
            'vendor',
        ]

        labels = {
            'payment_id': 'Payment ID ',
            'date': "Payment Date",
            'invoice': 'Invoice ID ',
            'vendor': 'Vendor',
        }

        widgets = { 
            'payment_id' : forms.TextInput(attrs={'class' : 'form-control'}),
            'date' : forms.NumberInput(attrs={'type': 'date'}),
            'invoice' : forms.Select(attrs={'class' : 'form-control'}),
            'vendor' : forms.Select(attrs={'class' : 'form-control'}),
        }
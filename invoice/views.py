from django.shortcuts import render
<<<<<<<<< Temporary merge branch 1

# Create your views here.
=========
# Create your views here.

def home(request):
    return render(request, 'invoice/home.html')
>>>>>>>>> Temporary merge branch 2

class InvoiceDetailView(DetailView):
    model = Invoice
from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpRequest
from datetime import datetime

from django.contrib.auth.decorators import login_required


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated:
        return render(request,'invoice/home.html')
    else:
        return render(
            request,
            'invoice/base.html',
            {
                'title':'Home Page',
                'year': datetime.now().year,
            }
        )

@login_required
def menu(request):
    check_employee = request.user.groups.filter(name='employee').exists()

    context = {
            'title':'Main Menu',
            'is_employee': check_employee,
            'year':datetime.now().year,
        }
    context['user'] = request.user

    return render(request,'invoice/home.html',context)
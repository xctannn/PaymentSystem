from django.shortcuts import render,redirect
from account.models import EmployeeProfile, VendorProfile
from .models import Notification
from django.contrib.auth.decorators import login_required

def is_CFO(User):
    return User.groups.filter(name='CFO').exists()

def is_FO(User):
    return User.groups.filter(name='Finance Officer').exists()

def is_vendor(User):
    return User.groups.filter(name='Vendor').exists()

@login_required
def GetNotifications(request):
    if is_CFO(request.user) or is_FO(request.user):
        employee = EmployeeProfile.objects.get(user = request.user)
        notifications = Notification.objects.filter(employee_receiver=employee).order_by('-date') 
    if is_vendor(request.user):
        vendor = VendorProfile.objects.get(user = request.user)
        notifications = Notification.objects.filter(vendor_receiver=vendor).order_by('-date') 
        
    context = {
        'notifications': notifications
    }
    if is_CFO(request.user):
        context['CFO'] = "CFO"
    return render(request, 'notification/home.html', context)


@login_required
def DeleteNotification(request, noti_id):
    if is_CFO(request.user) or is_FO(request.user):
        employee = EmployeeProfile.objects.get(user = request.user)
        Notification.objects.filter(employee_receiver=employee, id=noti_id).delete() 
    if is_vendor(request.user):
        vendor = VendorProfile.objects.get(user = request.user)
        Notification.objects.filter(vendor_receiver=vendor, id=noti_id).delete() 
    return redirect('notification-home')

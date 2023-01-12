from django.shortcuts import render,redirect


from .models import Notification
# Create your views here.
def GetNotifications(request):
    user = request.user
    notifications = Notification.objects.order_by('-date') #filter(reciver=user)
    
    context = {
        'notifications': notifications
    }

    return render(request, 'notification/home.html', context)

def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id).delete() #filter(reciver=user)
    return redirect('notification-home')

def CountNotifications(request):
    count_notifications = None
    if request.user.is_authenticated:
        count_notifications = Notification.objects.filter(user=request.user).count()
    return {'count_notifications': count_notifications}
from django.db import models
from django.contrib.auth.models import User
from invoice.models import Invoice
from receipt.models import Receipt
from payment.models import Payment

# Create your models here.
class Notification(models.Models):
    NOTIFICATION_TYPES = (
                        (1, "Payment"),
                        (2, "Edit Request"),
                        (3, "Edit Approval"),
                        (4, "Verification Request"),
                        (5, "Verification Approval")
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="noti_invoice", blank=True, null=True)
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE, related_name="noti_receipt", blank=True, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name="noti_payment", blank=True, null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_receiver")
    notification_type = models.IntegerField(choices = NOTIFICATION_TYPES)
    sucesss = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    

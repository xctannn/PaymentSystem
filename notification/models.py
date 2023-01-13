from django.db import models
from account.models import EmployeeProfile, VendorProfile

class Notification(models.Model):
    NOTIFICATION_TYPES = (
                        (1, "Payment"),
                        (2, "Edit Request"),
                        (3, "Edit Approval"),
                        (4, "Verification Request"),
                        (5, "Verification Approval")
    )

    notification_type = models.IntegerField(choices = NOTIFICATION_TYPES)
    invoice = models.ForeignKey('invoice.Invoice', on_delete=models.CASCADE, related_name="noti_invoice", blank=True, null=True)
    invoice_edit = models.ForeignKey('invoice.InvoiceEdit', on_delete=models.CASCADE, related_name="noti_invoice", blank=True, null=True)
    receipt = models.ForeignKey('receipt.Receipt', on_delete=models.CASCADE, related_name="noti_receipt", blank=True, null=True)
    receipt_edit = models.ForeignKey('receipt.ReceiptEdit', on_delete=models.CASCADE, related_name="noti_receipt", blank=True, null=True)
    payment = models.ForeignKey('payment.Payment', on_delete=models.CASCADE, related_name="noti_receipt", blank=True, null=True)
    employee_receiver = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="noti_receiver", null=True)
    vendor_receiver = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name="noti_receiver", null=True)
    success = models.BooleanField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    

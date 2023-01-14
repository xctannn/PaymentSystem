from django.db import models
from account.models import EmployeeProfile, VendorProfile
from invoice.models import Invoice
from notification.models import Notification

class Payment(models.Model):
    payment_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    uploader = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING, blank=True, null=True)
    verification_status = models.BooleanField(blank=True, null=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)

    def get_vendor_name(self):
        return self.vendor.name

    def get_vendor_address(self):
        return self.vendor.address

    def get_invoice_id(self):
        return self.invoice.invoice_id
    
    def get_amount_paid(self):
        return self.invoice.amount_owed

    def get_uploader_name(self):
        return (self.uploader.first_name + " " + self.uploader.last_name)

    def set_uploader(self, uploader):
        self.uploader = uploader
        self.save(update_fields=["uploader"])

    def __str__(self):
        return self.payment_id

    def verify(self):
        self.verification_status = True
        self.save(update_fields=["verification_status"])

    def deny(self):
        self.verification_status = False
        self.save(update_fields=["verification_status"])

    def send_verification_request(self):
        notify = Notification(payment=self, notification_type=4, vendor_receiver=self.vendor)
        notify.save()

    def send_verification_approval(self):
        CFOs = EmployeeProfile.objects.filter(position='CFO')
        for CFO in CFOs:
            notify = Notification(payment=self, notification_type=5, success=True, employee_receiver=CFO)
            notify.save()
    
    def send_verification_denial(self):
        CFOs = EmployeeProfile.objects.filter(position='CFO')
        for CFO in CFOs:
            notify = Notification(payment=self, notification_type=5, success=False, employee_receiver=CFO)
            notify.save()
    


    
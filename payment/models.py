from django.db import models
from account.models import EmployeeProfile, VendorProfile
from invoice.models import Invoice

# Create your models here.

class Payment(models.Model):
    payment_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    uploader = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING)
    
    def get_vendor_name(self):
        return self.vendor.name

    def get_vendor_address(self):
        return self.vendor.address

    def get_invoice_id(self):
        return self.invoice.invoice_id
    
    def get_amount_paid(self):
        return self.invoice.amount_owned

    def get_uploader_name(self):
        return (self.uploader.first_name + " " + self.uploader.last_name)
    
    def get_department(self):
        return self.invoice.department

    def __str__(self):
        return self.payment_id
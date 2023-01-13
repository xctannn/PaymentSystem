from django.db import models
from account.models import EmployeeProfile, VendorProfile
from invoice.models import Invoice

class Receipt(models.Model):
    receipt_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    uploader = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING, blank=True, null=True)
    department = models.CharField(max_length=50, choices=EmployeeProfile.Department.choices, blank=True)

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

    def set_department(self):
        self.department = self.invoice.department
        self.save(update_fields=["department"])

    def set_uploader(self, uploader):
        self.uploader = uploader
        self.save(update_fields=["uploader"])

    def __str__(self):
        return self.receipt_id


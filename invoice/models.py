from django.db import models
from account.models import EmployeeProfile, VendorProfile
import datetime

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    due_date = models.DateField()
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.IntegerField(null=True)
    amount_owned = models.DecimalField(max_digits=10, decimal_places=2)
    uploader = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING, blank=True, null=True)
    department = models.CharField(max_length=50, choices=EmployeeProfile.Department.choices, blank=True)
    first_CFO_approved = models.BooleanField(default=False)
    second_CFO_approved = models.BooleanField(default=False)
    approved_date = models.DateField(null=True, blank=True)

    def get_uploader_name(self):
        return (self.uploader.first_name + " " + self.uploader.last_name)

    def get_vendor_name(self):
        return self.vendor.name

    def get_vendor_address(self):
        return self.vendor.address

    def set_uploader(self, uploader):
        self.uploader = uploader
        self.save(update_fields=["uploader"])

    def set_department(self):
        self.department = self.uploader.department
        self.save(update_fields=["department"])

    def set_approved_date(self):
        self.approved_date = datetime.date.today()
        self.save(update_fields=["approved_date"])

    def set_first_CFO_approve(self):
        self.first_CFO_approved = True
        self.save(update_fields=["first_CFO_approved"])
    
    def set_second_CFO_approve(self):
        self.second_CFO_approved = True
        self.save(update_fields=["second_CFO_approved"])

    def get_first_CFO_name(self):
        CFO = EmployeeProfile.objects.filter(position='CFO').first()
        return CFO.first_name + " " + CFO.last_name

    def get_second_CFO_name(self):
        CFO = EmployeeProfile.objects.filter(position='CFO').last()
        return CFO.first_name + " " + CFO.last_name

    def get_item_list(self):
        return Item.objects.filter(invoice = self.invoice_id).order_by('-pk')

    def __str__(self):
        return self.invoice_id


class Item(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

    def get_invoice_id(self):
        return self.invoice.invoice_id
    
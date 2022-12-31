from django.db import models
from account.models import EmployeeProfile, VendorProfile

class Item(models.Model):
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    due_date = models.DateField()
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    item = models.ManyToManyField(Item)
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.IntegerField(null=True)
    amount_owned = models.DecimalField(max_digits=10, decimal_places=2)
    uploader = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING)
    department = models.CharField(max_length=50, choices=EmployeeProfile.Department.choices, blank=True)
    first_CFO_Approved = models.BooleanField(default=False)
    second_CFO_Approved = models.BooleanField(default=False)

    @property
    def get_uploader_name(self):
        return (self.uploader.first_name + " " + self.uploader.last_name)

    @property
    def get_vendor_name(self):
        return self.vendor.name

    @property
    def get_item_list(self):
        return (self.item.all())

    def set_department(self):
        self.department = self.uploader.department

    def __str__(self):
        return self.invoice_id

from django.db import models
from account.models import EmployeeProfile, VendorProfile
from invoice.models import Invoice

class Receipt(models.Model):
    receipt_id = models.CharField(max_length=20, primary_key=True)
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
        return self.invoice.amount_owed

    def get_uploader_name(self):
        return (self.uploader.first_name + " " + self.uploader.last_name)
    
    def get_department(self):
        return self.invoice.department

    def __str__(self):
        return self.receipt_id

class ReceiptEdit(models.Model):
    original_receipt_id = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    date = models.DateField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    editor = models.ForeignKey(EmployeeProfile, on_delete=models.DO_NOTHING)
    
    def get_vendor_name(self):
        return self.vendor.name

    def get_vendor_address(self):
        return self.vendor.address

    def get_invoice_id(self):
        return self.invoice.invoice_id
    
    def get_amount_paid(self):
        return self.invoice.amount_owed

    def get_editor_name(self):
        return (self.editor.first_name + " " + self.editor.last_name)
    
    def get_department(self):
        return self.invoice.department

    def set_original_receipt_id(self, invoice):
        self.invoice = invoice
        self.save(update_fields=["invoice"])

    def set_editor(self, user):
        self.editor = user

    def __str__(self):
        return str(self.pk)

    def editOriginalReceipt(self):
        self.original_receipt_id.date = self.date
        self.original_receipt_id.vendor = self.vendor
        self.original_receipt_id.save(update_fields=['date', 'vendor'])

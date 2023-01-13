from django.db import models
from account.models import EmployeeProfile, VendorProfile, User
from notification.models import Notification
import datetime

class Invoice(models.Model):
    invoice_id = models.CharField(max_length=20, primary_key=True)
    date = models.DateField()
    due_date = models.DateField()
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.IntegerField(null=True)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
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

    def send_invoice_payment_request_notification_to_other_CFO(self, CFO):
        user = User.objects.get(username=CFO.user)
        otherCFO = EmployeeProfile.objects.filter(position='CFO').exclude(user=user).first()
        notify  = Notification(invoice=self, notification_type=1, employee_receiver=otherCFO)
        notify.save()
    
    def send_invoice_payment_request_notification_to_all_CFO(self):
        CFOs = EmployeeProfile.objects.filter(position='CFO')
        for CFO in CFOs:
            notify  = Notification(invoice=self, notification_type=1, employee_receiver=CFO)
            notify.save()

    def send_invoice_payment_approval_notification(self):
        notify = Notification(invoice=self, notification_type=1, success = True, employee_receiver=self.uploader) 
        notify.save()
    
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

class InvoiceEdit(models.Model):
    original_invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    due_date = models.DateField()
    vendor = models.ForeignKey(VendorProfile, on_delete=models.DO_NOTHING)
    amount_charged = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.IntegerField(null=True)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    editor = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, blank=True, null=True)

    def get_department(self):
        return self.original_invoice_id.department

    def get_vendor_name(self):
        return self.vendor.name

    def get_vendor_address(self):
        return self.vendor.address

    def get_date(self):
        return self.original_invoice_id.date

    def get_editor_name(self):
        return (self.editor.first_name + " " + self.editor.last_name)

    def get_item_list(self):
        return ItemEdit.objects.filter(invoice_edit = self.pk).order_by('-pk')

    def set_editor(self, editor):
        self.editor = editor
        self.save(update_fields=["editor"])

    def edit_original_invoice(self):
        self.original_invoice_id.due_date = self.due_date
        self.original_invoice_id.vendor = self.vendor
        self.original_invoice_id.amount_charged = self.amount_charged
        self.original_invoice_id.tax = self.tax
        self.original_invoice_id.amount_owed = self.amount_owed
        self.original_invoice_id.save(update_fields=["due_date", "vendor", "amount_charged", "tax", "amount_owed"])

    def __str__(self):
        return str(self.pk)

    def send_request_notification(self):
        CFOs = EmployeeProfile.objects.filter(position='CFO')
        for CFO in CFOs:
            notify  = Notification(invoice_edit=self, notification_type=2, employee_receiver = CFO)  
            notify.save()

    def send_request_approval_notification(self):
        notify = Notification(invoice=self.original_invoice_id, notification_type=3, success = True, employee_receiver=self.editor)
        notify.save()
    
    def send_request_deny_notification(self):
        notify = Notification(invoice=self.original_invoice_id, notification_type=3, success = False, employee_receiver=self.editor)
        notify.save()
        
class ItemEdit(models.Model):
    original_item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    invoice_edit = models.ForeignKey(InvoiceEdit, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def edit_original_item(self):
        self.original_item_id.name = self.name
        self.original_item_id.unit_price = self.unit_price
        self.original_item_id.quantity = self.quantity
        self.original_item_id.total_price = self.total_price
        self.original_item_id.save(update_fields=["name", "unit_price", "quantity", "total_price"])

    def __str__(self):
        return self.name

    def get_invoice_id(self):
        return str(self.pk)
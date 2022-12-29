from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", 'ADMIN'
        EMPLOYEE = "EMPLOYEE", 'EMPLOYEE'
        VENDOR = "VENDOR",'VENDOR'

    base_role = Role.ADMIN

    role = models.CharField(_("Role"), max_length=50, choices=Role.choices, default=base_role)

    def save(self, *args, **kwargs):
        if not self.id:
            self.role = self.base_role
        return super().save(*args, **kwargs)


class EmployeeManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.EMPLOYEE)


class VendorManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Role.VENDOR)


class Employee(User):
    base_role = User.Role.EMPLOYEE
    objects = EmployeeManager()

    class Meta:
        proxy = True


class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Position(models.TextChoices):
        CFO = 'CFO'
        FINANCE_OFFICER = 'Finance Officer'
    
    class Department(models.TextChoices):
        HR = 'Human Resources'
        IT = 'IT'
        RnD = 'Research and Development'
        Marketing = 'Marketing'
        Production = 'Production'

    employee_id = models.CharField(max_length=5, primary_key= True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    position = models.CharField(max_length=20, choices=Position.choices)
    department = models.CharField(max_length=50, choices=Department.choices, blank=True)


class Vendor(User):
    base_role = User.Role.VENDOR
    objects = VendorManager()

    class Meta:
        proxy = True


class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.TextField()


# @receiver(post_save, sender=Employee)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "EMPLOYEE":
#         EmployeeProfile.objects.create(user=instance)

# @receiver(post_save, sender=Vendor)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "VENDOR":
#         VendorProfile.objects.create(user=instance)
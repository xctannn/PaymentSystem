# Generated by Django 4.0.4 on 2023-01-13 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('payment', '0001_initial'),
        ('receipt', '0001_initial'),
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.IntegerField(choices=[(1, 'Payment'), (2, 'Edit Request'), (3, 'Edit Approval'), (4, 'Verification Request'), (5, 'Verification Approval')])),
                ('success', models.BooleanField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('employee_receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_receiver', to='account.employeeprofile')),
                ('invoice', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_invoice', to='invoice.invoice')),
                ('invoice_edit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_invoice', to='invoice.invoiceedit')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_receipt', to='payment.payment')),
                ('receipt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_receipt', to='receipt.receipt')),
                ('receipt_edit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_receipt', to='receipt.receiptedit')),
                ('vendor_receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='noti_receiver', to='account.vendorprofile')),
            ],
        ),
    ]

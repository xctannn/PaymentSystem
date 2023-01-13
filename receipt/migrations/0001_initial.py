# Generated by Django 4.0.4 on 2023-01-13 10:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('receipt_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('department', models.CharField(blank=True, choices=[('Human Resources', 'Hr'), ('IT', 'It'), ('Research and Development', 'Rnd'), ('Marketing', 'Marketing'), ('Production', 'Production')], max_length=50)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.employeeprofile')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.vendorprofile')),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptEdit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('editor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.employeeprofile')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
                ('original_receipt_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='receipt.receipt')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.vendorprofile')),
            ],
        ),
    ]

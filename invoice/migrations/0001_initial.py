# Generated by Django 4.0.4 on 2023-01-13 05:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('due_date', models.DateField()),
                ('amount_charged', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.IntegerField(null=True)),
                ('amount_owed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('department', models.CharField(blank=True, choices=[('Human Resources', 'Hr'), ('IT', 'It'), ('Research and Development', 'Rnd'), ('Marketing', 'Marketing'), ('Production', 'Production')], max_length=50)),
                ('first_CFO_approved', models.BooleanField(default=False)),
                ('second_CFO_approved', models.BooleanField(default=False)),
                ('approved_date', models.DateField(blank=True, null=True)),
                ('uploader', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='account.employeeprofile')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.vendorprofile')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceEdit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('amount_charged', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tax', models.IntegerField(null=True)),
                ('amount_owed', models.DecimalField(decimal_places=2, max_digits=10)),
                ('editor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.employeeprofile')),
                ('original_invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.vendorprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='ItemEdit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoice')),
                ('invoice_edit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.invoiceedit')),
                ('original_item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.item')),
            ],
        ),
    ]

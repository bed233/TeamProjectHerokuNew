# Generated by Django 4.0.3 on 2022-03-25 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allergy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='allergy_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='menu_images/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('calories', models.CharField(blank=True, max_length=10, null=True)),
                ('allergy', models.ManyToManyField(related_name='item', to='customer.allergy')),
                ('category', models.ManyToManyField(related_name='item', to='customer.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('email', models.CharField(blank=True, max_length=100)),
                ('order_confirmed', models.BooleanField(default=False)),
                ('is_paid', models.BooleanField(default=False)),
                ('ready_to_deliver', models.BooleanField(default=False)),
                ('is_delivered', models.BooleanField(default=False)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('need_help', models.BooleanField(default=False)),
                ('table_number', models.IntegerField(default=0)),
                ('items', models.ManyToManyField(blank=True, related_name='order', to='customer.menuitem')),
            ],
        ),
        migrations.CreateModel(
            name='ItemQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderID', models.IntegerField(default=0)),
                ('quantity', models.IntegerField(default=0)),
                ('totalPrice', models.DecimalField(decimal_places=2, max_digits=7)),
                ('item', models.ManyToManyField(blank=True, related_name='ItemOrder', to='customer.menuitem')),
            ],
        ),
    ]
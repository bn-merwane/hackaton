# Generated by Django 5.1.2 on 2024-11-20 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('client', 'Client'), ('employee', 'Employee'), ('facteur', 'Facteur')], max_length=20),
        ),
    ]

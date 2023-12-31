# Generated by Django 4.2.6 on 2023-11-03 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_return'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='return',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='return',
            name='user',
        ),
        migrations.AddField(
            model_name='return',
            name='admin_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='return',
            name='requested_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='return',
            name='status',
            field=models.CharField(default='на розгляді', max_length=20),
        ),
    ]

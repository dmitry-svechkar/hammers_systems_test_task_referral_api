# Generated by Django 5.0.4 on 2024-04-20 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='confirmation code'),
        ),
    ]
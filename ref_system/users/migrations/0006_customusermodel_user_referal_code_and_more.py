# Generated by Django 5.0.4 on 2024-04-21 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_customusermodel_groups_customusermodel_is_superuser_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customusermodel',
            name='user_referal_code',
            field=models.CharField(max_length=6, null=True, verbose_name='Реферальный код'),
        ),
        migrations.AlterField(
            model_name='customusermodel',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='Код потверждения'),
        ),
        migrations.AlterField(
            model_name='customusermodel',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]

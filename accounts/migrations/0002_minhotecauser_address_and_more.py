# Generated by Django 4.0.2 on 2022-06-15 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='minhotecauser',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='address_complement',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='address_number',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='can_borrow',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='contact_phone',
            field=models.CharField(max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='neighborhood',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='state',
            field=models.CharField(default='SP', max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='minhotecauser',
            name='zip_code',
            field=models.CharField(max_length=8, null=True),
        ),
    ]

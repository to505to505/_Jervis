# Generated by Django 4.1.3 on 2023-04-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0004_image_is_ended'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='updated_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='messageid_sseed',
            field=models.CharField(max_length=70, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='image',
            name='tg_message_id',
            field=models.CharField(max_length=70, null=True, unique=True),
        ),
    ]
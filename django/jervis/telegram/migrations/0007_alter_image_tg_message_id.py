# Generated by Django 4.1.3 on 2023-04-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram', '0006_alter_image_image_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='tg_message_id',
            field=models.IntegerField(max_length=70, null=True),
        ),
    ]

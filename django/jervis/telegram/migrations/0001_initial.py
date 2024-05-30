# Generated by Django 4.1.3 on 2023-04-22 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField(null=True, unique=True)),
                ('generation_amount', models.IntegerField(default=15)),
                ('status', models.CharField(choices=[('paid', 'paid'), ('free', 'free')], default='free', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telegram.chat')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(null=True)),
                ('tg_message_id', models.IntegerField(null=True)),
                ('messageid_sseed', models.CharField(max_length=200, null=True, unique=True)),
                ('prompt', models.TextField(db_index=True, null=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('is_ended', models.BooleanField(default=False)),
                ('chat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telegram.chat')),
                ('client', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='telegram.client')),
            ],
        ),
    ]

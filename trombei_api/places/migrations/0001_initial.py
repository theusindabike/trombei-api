# Generated by Django 4.1.6 on 2023-02-15 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('full_address', models.CharField(max_length=255, verbose_name='full_address')),
                ('image', models.ImageField(blank=True, null=True, upload_to='places')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Places', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DirectionUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('GOOGLE-MAPS', 'Google Maps'), ('UBER', 'Uber')], max_length=32, verbose_name='type')),
                ('url', models.URLField(max_length=512, verbose_name='url')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='direction_urls', to='places.place')),
            ],
        ),
    ]

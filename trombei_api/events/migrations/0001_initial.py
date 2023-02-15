# Generated by Django 4.1.6 on 2023-02-15 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128, verbose_name='title')),
                ('content', models.CharField(max_length=255, verbose_name='content')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PUBLISHED', 'Published')], max_length=32, verbose_name='type')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Events', to=settings.AUTH_USER_MODEL)),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='places.place')),
            ],
        ),
    ]

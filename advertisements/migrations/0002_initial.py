# Generated by Django 5.2 on 2025-05-01 17:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("advertisements", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="advertisement",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="advertisements",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец объявления",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="advertisement",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="advertisements.advertisement",
                verbose_name="Объявление",
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reviews",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Владелец отзыва",
            ),
        ),
    ]

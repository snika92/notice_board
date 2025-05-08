from django.db import models

from config import settings


class Advertisement(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название товара")
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание товара"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец объявления",
        related_name="advertisements",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время и дата создания объявления"
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]


class Comment(models.Model):
    text = models.TextField(null=True, blank=True, verbose_name="Текст отзыва")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Владелец отзыва",
        related_name="comments",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    advertisement = models.ForeignKey(
        Advertisement,
        verbose_name="Объявление",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Время и дата создания отзыва"
    )

    def __str__(self):
        return f"{self.pk}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

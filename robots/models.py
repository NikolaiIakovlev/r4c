from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Robot(models.Model):
    MODEL_CHOICES = [
        ('R2', 'R2'),
        ('13', '13'),
        ('X5', 'X5'),
        # ... 
    ]
    VERSION_CHOICES = [
        ('D2', 'D2'),
        ('XS', 'XS'),
        ('LT', 'LT'),
        # ... 
    ]
    serial = models.CharField(max_length=5, blank=False, null=False)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    in_stock = models.BooleanField(default=False) #добавлено поле наличия на складе

    def clean(self):
        """метод валидации. Проверяем корректность введенных данных"""
        if self.model not in [model[0] for model in self.MODEL_CHOICES]:
            raise ValidationError("Модель не найдена.")
        if self.version not in [version[0] for version in self.VERSION_CHOICES]:
            raise ValidationError("Версия не найдена.")
        if self.created > timezone.now():
            raise ValidationError("Дата создания не может быть в будущем.")

    def save(self, *args, **kwargs):
        self.full_clean() #вызываем валидацию перед сохранением
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('serial', 'model', 'version')

    def __str__(self):
        return f"Robot {self.serial} {self.model}-{self.version} created {self.created}"

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from .managers import PortUserManager
import uuid


class PortUser(AbstractUser):
    """Таблица пользователя"""
    username = None
    email = models.EmailField(_('email'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = PortUserManager()

    full_name = models.CharField(max_length=200, verbose_name='Полное имя')
    billing_address = models.CharField(max_length=200, verbose_name='Платежный адрес')
    confirm_user = models.UUIDField(default=uuid.uuid4, editable=False)
    user_ip = models.ManyToManyField('Ip', blank=True, verbose_name='Ip адрес пользователя')
    quantity_ip = models.IntegerField(null=True, blank=True, verbose_name='Колличество ip адресов')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Ip(models.Model):
    """Таблица ip адресов"""
    ip = models.GenericIPAddressField('Ip адрес')
    user = models.ManyToManyField(PortUser, verbose_name='Пользователь')
    quantity_user = models.IntegerField('Колличество пользователей')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'Ip адрес'
        verbose_name_plural = 'Ip адреса'


class SubscriptionTypes(models.Model):
    """Таблица типов подписки"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CargoTypes(models.Model):
    """Таблица типов груза"""
    name = models.CharField(max_length=100, verbose_name='Название груза')

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Таблица подписки"""
    user = models.ForeignKey(PortUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    cargo = models.ManyToManyField(CargoTypes, blank=True, verbose_name='Груз')
    subscription_types = models.ForeignKey(SubscriptionTypes, on_delete=models.CASCADE, verbose_name='Тип подписки')
    date_from = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала подписки')
    date_to = models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания подписки')

    def __str__(self):
        return self.subscription_types.name

    class Meta:
        verbose_name = 'Подписку'
        verbose_name_plural = 'Подписки'

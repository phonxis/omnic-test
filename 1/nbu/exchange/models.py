from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class ExchangeManager(models.Manager):
    def today(self):
        return self.filter(exchangedate=datetime.now())


class Exchange(models.Model):
    r030 = models.IntegerField(_("Код валюты"))
    cc = models.CharField(
        _("Код валюты буквенный"),
        max_length=5
    )
    txt = models.CharField(
        _("Название валюты"),
        max_length=128
    )
    rate = models.DecimalField(
        _("Значение"),
        max_digits=10,
        decimal_places=4
    )
    exchangedate = models.DateField(_("Дата"))

    objects = ExchangeManager()

    class Meta:
        verbose_name = _("Курс валюты")
        verbose_name_plural = _("Курс валют")
        unique_together = ("exchangedate", "cc")

    def __str__(self):
        return self.cc

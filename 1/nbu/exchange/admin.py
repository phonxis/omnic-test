from django.contrib import admin

from .models import Exchange

# Register your models here.


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
	list_display = ('cc', 'exchangedate', 'rate')
	list_filter = ('cc', )

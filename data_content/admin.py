from django.contrib import admin
from .models import StockMarketData
# Register your models here.


@admin.register(StockMarketData)
class StockMarketDataAdmin(admin.ModelAdmin):
    list_display = ["id", "date", "trade_code", "volume"]

from django.db import models

# Create your models here.


class StockMarketData(models.Model):
    trade_code = models.CharField(max_length=256)
    high = models.FloatField()
    low = models.FloatField()
    open = models.FloatField()
    close = models.FloatField()
    volume = models.CharField(max_length=256)
    date = models.DateField()

    class Meta:
        ordering = ("date",)

    def __str__(self) -> str:
        return str(self.date)


from datetime import datetime
from django.conf import settings
from data_content.models import StockMarketData
from django.core.management.base import BaseCommand

import json
import re

# load json data


class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'dataFile' / 'stock_market_data.json'

        with open(datafile) as f:
            data = json.load(f)
            regex = '[+-]?[0-9]+\.[0-9]+'

            for row in data:
                dt = datetime.strptime(row["date"], "%Y-%m-%d").date()
                if re.match(regex, row["high"]) and re.match(regex, row["low"]) and re.match(regex, row["open"]) and re.match(regex, row["close"]):
                    StockMarketData.objects.get_or_create(
                        date=dt,
                        trade_code=row["trade_code"],
                        high=row["high"],
                        low=row["low"],
                        open=row["open"],
                        close=row["close"],
                        volume=row["volume"]
                    )
        f.close()

from django import forms
from .models import StockMarketData


class StockMarketDataForm(forms.ModelForm):
    class Meta:
        model = StockMarketData
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StockMarketDataForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'form-control p-2 my-2'})

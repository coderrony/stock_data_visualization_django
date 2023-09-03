from django.shortcuts import render, redirect
from .models import StockMarketData
from .forms import StockMarketDataForm
from django.contrib import messages

import plotly.express as px

# Create your views here.


def home(request):

    # stock_data = StockMarketData.objects.order_by(
    #     "-date")[:5]
    stock_data = StockMarketData.objects.all()

    unique_trade_codes = StockMarketData.objects.values_list(
        'trade_code', flat=True).distinct()
    trade_code = request.GET.get("trade_code")

    if trade_code:
        stock_data = StockMarketData.objects.filter(trade_code=trade_code)

    fig = px.line(
        x=[d.date for d in stock_data],
        y=[v.volume for v in stock_data],
        title="Data Visualization ",
        labels={"x": "Date", 'y': "Volume"}
    )

    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })

    chart = fig.to_html()
    return render(request, "index.html", context={"stock_data": stock_data, "chart": chart, "unique_trade_codes": unique_trade_codes})


def update_stock(request, pk):
    stock = StockMarketData.objects.get(pk=pk)
    form = StockMarketDataForm(instance=stock)
    if request.method == "POST":
        form = StockMarketDataForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Update Successfully!")
            return redirect("home")
    return render(request, "update_stock.html", context={"form": form})


def delete_stock(request, pk):
    stock = StockMarketData.objects.get(pk=pk)
    stock.delete()
    messages.warning(request, "Delete Successfully!")
    return redirect("home")

from django.shortcuts import render, redirect
from .models import StockMarketData
from .forms import StockMarketDataForm
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator
import plotly.express as px


# Create your views here.


def home(request):

    # Retrieve all stock data
    all_stock_data = StockMarketData.objects.order_by("-date")

    # Create a Paginator instance
    paginator = Paginator(all_stock_data, per_page=20)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Get the Page object for the current page
    stock_data = paginator.get_page(page_number)

    # convert pagination data to queryset
    stock_data_queryset = stock_data.object_list

    # create stock
    form = StockMarketDataForm()
    if request.method == "POST":
        form = StockMarketDataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Stock Create Successfully")
            return redirect("home")

    # sort every distinct trade_code value
    unique_trade_codes = StockMarketData.objects.values_list(
        'trade_code', flat=True).distinct()

    # receive trade_code request
    trade_code = request.GET.get("trade_code")
    if trade_code:
        stock_data_queryset = StockMarketData.objects.filter(
            trade_code=trade_code)

        stock_data = stock_data_queryset

    # data insert in line chart vertical and horizontal
    fig = px.line(
        x=[d.date for d in stock_data_queryset],
        y=[v.volume for v in stock_data_queryset],
        title="Data Visualization ",
        labels={"x": "Date", 'y': "Volume"}
    )

    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5
    })

    chart = fig.to_html()
    return render(request, "index.html", context={"stock_data": stock_data, "chart": chart, "unique_trade_codes": unique_trade_codes, "form": form})


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


# all stock show
def all_stock(request):
    stock_data = StockMarketData.objects.all()

    # sort every distinct trade_code value
    unique_trade_codes = StockMarketData.objects.values_list(
        'trade_code', flat=True).distinct()

    # data insert in line chart
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

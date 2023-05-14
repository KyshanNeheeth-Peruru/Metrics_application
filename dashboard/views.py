from django.shortcuts import render
import matplotlib.pyplot as plt
from .models import Temperature, pH, DistilledOxygen, Pressure
from django.urls import reverse
from django.http import HttpResponse
from django.template import loader
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import csv
import base64
import matplotlib
import matplotlib.pyplot as plt
import io
import urllib
from datetime import datetime, timedelta
from django.core.paginator import Paginator

# Create your views here.
def plot_graph(data, name):
    x = [d.time for d in data]
    y = [d.value for d in data]
    # Create a new figure and set the title
    plt.figure()
    plt.xlabel("Date & time")
    plt.ylabel(name)
    # Plot the temperature data
    if len(data) == 1:
        plt.scatter(x, y)
    else:
        plt.plot(x, y)
    # plt.plot(x, y)
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    # Encode the buffer in base64
    graph = urllib.parse.quote(base64.b64encode(buf.read()))
    return graph

def dashboard(request):
    if request.GET.get('start-time') and request.GET.get('end-time'):
        start_time = datetime.strptime(request.GET.get('start-time'), '%Y-%m-%dT%H:%M')
        end_time = datetime.strptime(request.GET.get('end-time'), '%Y-%m-%dT%H:%M')
        temperature_data = Temperature.objects.filter(time__range=(start_time, end_time)).order_by('time')
        pH_data = pH.objects.filter(time__range=(start_time, end_time)).order_by('time')
        DistilledOxygen_data = DistilledOxygen.objects.filter(time__range=(start_time, end_time)).order_by('time')
        Pressure_data = Pressure.objects.filter(time__range=(start_time, end_time)).order_by('time')
    else:
        temperature_data = Temperature.objects.all().order_by('time')
        pH_data = pH.objects.all().order_by('time')
        DistilledOxygen_data = DistilledOxygen.objects.all().order_by('time')
        Pressure_data = Pressure.objects.all().order_by('time')
        
    paginator_temp = Paginator(temperature_data, 10) # Show 10 temperatures per page
    page_number_temp = request.GET.get('page_temp')
    page_obj_temp = paginator_temp.get_page(page_number_temp)
    
    paginator_ph = Paginator(pH_data, 10) # Show 10 temperatures per page
    page_number_ph = request.GET.get('page_ph')
    page_obj_ph = paginator_ph.get_page(page_number_ph)
    
    paginator_do2 = Paginator(DistilledOxygen_data, 10) # Show 10 temperatures per page
    page_number_do2 = request.GET.get('page_do2')
    page_obj_do2 = paginator_do2.get_page(page_number_do2)
    
    paginator_pressure = Paginator(Pressure_data, 10) # Show 10 temperatures per page
    page_number_pressure = request.GET.get('page_pressure')
    page_obj_pressure = paginator_pressure.get_page(page_number_pressure)

    temp_graph = plot_graph(temperature_data, "Temperature (Celsius)")
    ph_graph = plot_graph(pH_data, "pH")
    distO2_graph = plot_graph(DistilledOxygen_data, "Distilled O2 (%)")
    pressure_graph = plot_graph(Pressure_data, "Pressure (psi)")
    return render(request, 'dashboard.html', {'temps': page_obj_temp, 'phs': page_obj_ph,'distOs': page_obj_do2,'pressures': page_obj_pressure, 'temp_graph': temp_graph, 'ph_graph': ph_graph, 'distO2_graph': distO2_graph, 'pressure_graph': pressure_graph})

def temperature_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="temperature.csv"'
    writer = csv.writer(response)
    writer.writerow(['Temperature', 'Date/Time'])
    for item in Temperature.objects.all():
        writer.writerow([item.value, item.time])
    return response

def ph_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ph.csv"'
    writer = csv.writer(response)
    writer.writerow(['pH', 'Date/Time'])
    for item in pH.objects.all():
        writer.writerow([item.value, item.time])
    return response

def distilledOxygen_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="distilledOxygen.csv"'
    writer = csv.writer(response)
    writer.writerow(['DistilledOxygen', 'Date/Time'])
    for item in DistilledOxygen.objects.all():
        writer.writerow([item.value, item.time])
    return response

def pressure_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pressure.csv"'
    writer = csv.writer(response)
    writer.writerow(['Pressure', 'Date/Time'])
    for item in Pressure.objects.all():
        writer.writerow([item.value, item.time])
    return response

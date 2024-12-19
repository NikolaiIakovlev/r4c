from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('', views.generate_excel_report, name='generate_excel_report'),
    ]
from django.urls import path
from . import views

app_name = 'robots'


urlpatterns = [
    path('robots/', views.create_robot, name='create_robot'),
]
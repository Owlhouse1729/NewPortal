from django.urls import path
from . import views

app_name = 'cafeteria'

urlpatterns = [
    path('', views.Top.as_view(), name='top'),
    path('reserve', views.Reserve.as_view(), name='reserve'),
    path('check', views.Check.as_view(), name='check'),
]

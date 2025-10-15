from django.urls import path
from . import views

app_name = 'journal'

urlpatterns = [
    path('unlock/', views.unlock, name='unlock'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_trade, name='add_trade'),
]

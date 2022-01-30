from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('probabilities/', views.probabilities, name='probabilities'),
    path('one_variable_stats/', views.one_variable_stats, name='one_variable_stats'),
]
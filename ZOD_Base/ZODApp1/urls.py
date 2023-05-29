from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from ZODApp1 import views
from .views import *


urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('otp', views.otp, name="otp"),
    path('activation', views.activation, name="activation"),
    path('generate_ticket_pc', views.generate_ticket_pc, name="generate_ticket_pc"),
    path('generate_ticket_ts', views.generate_ticket_ts, name="generate_ticket_ts"),
    path('print_ticket', views.print_ticket, name="print_ticket"),
    path('statement', views.statement, name="statement"),
    path('counter_close', views.counter_close, name="counter_close"),
    path('preview_closing', views.preview_closing, name="preview_closing"),
    path('collection', views.collection, name="collection"),
    path('summary', views.summary, name="summary"),
]


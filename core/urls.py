from django.urls import path
from . import views

urlpatterns = [
    path('',views.ReporteFacturaPDF.as_view(), name = 'index'),
]
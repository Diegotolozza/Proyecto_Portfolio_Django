from django.urls import path
from . import views

app_name = 'landing'
#agregué slug
urlpatterns = [
    path('', views.mostrar_portfolio, name='mostrar_portfolio'),
    path('categoria/<slug:slug>/', views.categoria_detalle, name='categoria_detalle'),
    path('contacto/', views.contacto, name='contacto'),
]

from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Foto
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings

# Create your views here.
def mostrar_portfolio(request):
    categorias = Categoria.objects.all()
    return render(request, 'index.html', {"categorias": categorias})

def categoria_detalle(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    fotos = categoria.fotos.all()
    return render(request, 'categoria.html', {"categoria": categoria, "fotos": fotos})

def contacto(request):
    enviado = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            mensaje = form.cleaned_data['mensaje']

            # Enviar email
            send_mail(
                subject=f"Nuevo mensaje de {nombre}",
                message=f"De: {nombre} <{email}>\n\n{mensaje}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],  # vos recibís el mail
                fail_silently=False,
            )
            enviado = True
            form = ContactForm()  # limpia el formulario
    else:
        form = ContactForm()
    return render(request, 'landing/contacto.html', {'form': form, 'enviado': enviado})
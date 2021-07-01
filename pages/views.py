from django.shortcuts import render, get_object_or_404
from .models import Pages,Contact

def pages(request,slug):
    """Представление статических страниц, и их данные"""
    page_data = get_object_or_404(Pages,slug=slug)
    context = {'page_data':page_data}
    return render(request,'pages/list_page.html',context)

def contacts(request):
    """Представление контактов"""
    contacts = Contact.objects.get(pk=1)
    context = {'contacts':contacts}
    return render(request,'pages/contacts.html',context)
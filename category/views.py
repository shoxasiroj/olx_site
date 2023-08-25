from django.shortcuts import render
from .models import ChildCategory


def olx_context_processor(request):
    context = {}
    context['categories'] = ChildCategory.objects.all()
    return context


def by_categories(request, pk):
    pass

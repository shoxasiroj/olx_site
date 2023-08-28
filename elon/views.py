from django.shortcuts import render, get_object_or_404
from .models import Elon

def detail(request, category_pk, pk):
    elon = Elon.objects.get(pk=pk)
    addimages = elon.additionalimage_set.all()
    context = {
        "elon": elon,
        'addimages': addimages
    }
    return render(request, 'main/detail.html', context)

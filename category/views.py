from django.shortcuts import render, get_object_or_404
from .models import ChildCategory
from django.core.paginator import Paginator
from django.db.models import Q
from elon.forms import SearchForm
from elon.models import Elon


# hammas templatesga categories keyword all ni yo`borish uchun
def olx_context_processor(request):
    context = {}
    context['categories'] = ChildCategory.objects.all()
    context['keyword'] = ""
    context['all'] = ''
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            context['keyword'] = '?keyword=' + keyword
            context['all'] = context['keyword']
    if 'page' in request.GET:
        page = request.GET['page']
        if page != 1:
            if context['all']:
                context['all'] += '&page=' + page
            else:
                context['all'] = '?page=' + page

    return context


# Categoryni bosgan vaqtimiz misol uydi bossak faqat uy chiqishi uchun
def by_categories(request, pk):
    category = get_object_or_404(ChildCategory, pk=pk)
    elonlar = Elon.objects.filter(is_active=True, category=pk)
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        q = Q(title__icontains=keyword)|Q(body__icontains=keyword)
        elonlar = elonlar.filter(q)
    else:
        keyword = ''
    form = SearchForm(initial={'keyword':keyword})
    paginator = Paginator(elonlar, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {
        "category": category,
        'page': page,
        'elonlar': page.object_list,
        'form': form
    }
    return render(request, 'main/by_category.html', context)

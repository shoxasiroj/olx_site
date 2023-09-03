from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Elon
from comment.models import Comment
from comment.forms import UserCommentForm, GuestCommentForm


# Detail uchun views
def detail(request, category_pk, pk):
    elon = Elon.objects.get(pk=pk)
    comments = Comment.objects.filter(elon=pk, is_active=True)
    initial = {'elon': elon.pk}
    if request.user.is_authenticated:
        initial['author'] = request.user.username
        form_class = UserCommentForm
    else:
        form_class = GuestCommentForm
    form = form_class(initial=initial)
    if request.method == 'POST':
        new_form = form_class(request.POST)
        if new_form.is_valid():
            new_form.save()
            messages.add_message(request, messages.SUCCESS, 'Commentariy qo`shildi')
        else:
            form = new_form
            messages.add_message(request, messages.WARNING, 'Commentariya qo`shilmadi')
    addimages = elon.additionalimage_set.all()
    context = {
        "elon": elon,
        'addimages': addimages,
        'form': form,
        'comments': comments
    }
    return render(request, 'main/detail.html', context)



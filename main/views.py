from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import AdvUser
from .forms import ChangeUserForm, RegisterUserForm
from .utilities import signer
from elon.models import Elon
from elon.forms import ElonCreateForm, AdditionalImageFormSet
from comment.models import Comment


def index(request):
    elonlar = Elon.objects.filter(is_active=True)[:10]
    context = {'elonlar': elonlar}
    return render(request, 'main/index.html', context)


@login_required
def profile(request):
    elonlar = Elon.objects.filter(author=request.user.pk) # faqatgina uziga tegishli elonlarni olish
    context = {'elonlar': elonlar}
    return render(request, 'main/profile.html', context)


# Biron bir elonnni ustiga bosgan vaqtimisz bizga tegishli elon haqidagi sahifaga utishimiz uchun
def profile_detail_elonlar(request, pk):
    elon = get_object_or_404(Elon, pk=pk)
    addimages = elon.additionalimage_set.all()
    comments = Comment.objects.filter(elon=pk, is_active=True)
    context = {
        'elon': elon,
        'addimages': addimages,
        'comments': comments,
    }
    return render(request, 'main/profile_detail_pk.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))


class OLXLoginView(LoginView):
    template_name = 'auth/login.html'



class OLXLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'auth/logout.html'


#Foydalanuvchi malumotlarini o`zgartirish uchun
class ChangeUserView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    form_class = ChangeUserForm
    template_name = 'main/change_user.html'
    success_url = reverse_lazy('profile')
    success_message = "Sizning ma`lumotlaringiz o`zgartirildi"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


# parolni o`zgartirish uchun
class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'main/password_change.html'
    success_url = reverse_lazy('profile')
    success_message = "Parolingiz o`zgartirildi"


# Registratsiyadan utish uchun
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'auth/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


#registratsiyadan utgandan keyin utganlik haqidagi malumotni chiqorish
class RegisterDoneView(TemplateView):
    template_name = 'auth/register_done.html'


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = AdvUser
    template_name = 'main/delete_user.html'
    success_url = reverse_lazy('index')

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, "Akkaunt o`chirildi")
        return super().post(request, *args, **kwargs)


# Pochtaga kelgan link orqali akkauntni aktiv qilish
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

@login_required
def profile_elon_create(request):
    if request.method == 'POST':
        form = ElonCreateForm(request.POST, request.FILES)
        if form.is_valid():
            elon = form.save()
            formset = AdditionalImageFormSet(request.POST, request.FILES, instance=elon)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Elon muvoffaqiyatli yaratildi')
                return redirect('profile')
    else:
        form = ElonCreateForm(initial={'author': request.user.pk})
        formset = AdditionalImageFormSet()
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'main/create_elon.html', context)

@login_required
def profile_elon_change(request, pk):
    elon = get_object_or_404(Elon, pk=pk)
    if request.method == 'POST':
        form = ElonCreateForm(request.POST, request.FILES, instance=elon)
        if form.is_valid():
            elon = form.save()
            formset = AdditionalImageFormSet(request.POST, request.FILES, instance=elon)
            if formset.is_valid():
                formset.save()
                messages.add_message(request, messages.SUCCESS, 'Elon muvoffaqiyatli o`zgartirildi')
                return redirect('profile')
    else:
        form = ElonCreateForm(instance=elon)
        formset = AdditionalImageFormSet(instance=elon)
    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'main/update_elon.html', context)


@login_required
def profile_elon_delete(request, pk):
    elon = get_object_or_404(Elon, pk=pk)
    if request.method == 'POST':
        elon.delete()
        messages.add_message(request, messages.SUCCESS, 'Elon o`chirildi')
        return redirect('profile')
    else:
        context = {
            'elon': elon
        }
    return render(request, 'main/delete_elon.html', context)

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.signing import BadSignature
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from .models import AdvUser
from .forms import ChangeUserForm, RegisterUserForm
from .utilities import signer


def index(request):
    return render(request, 'main/index.html')


@login_required
def profile(request):
    return render(request, 'main/profile.html')


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

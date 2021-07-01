from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import PortUser
from .forms import PortUserCreationForm, UserUpdateForm
from django.core.mail import send_mail
from .subscription import Subscrip


@login_required
def account(request):
    """Представление страницы профиля"""

    user = PortUser.objects.get(email=request.user)
    active_subscription = Subscrip(user).get_active_subscription
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST, instance=user)
        if user_update_form.is_valid():
            cd = user_update_form.cleaned_data
            user.email, user.full_name, user.billing_address = cd['email'], cd['full_name'], cd['billing_address']
            user.save()
    else:
        user_update_form = UserUpdateForm(instance=user)

    context = {'user_update_form': user_update_form, 'active_subscription': active_subscription}
    return render(request, 'account/account.html', context)


class SignUp(SuccessMessageMixin, CreateView):
    """Создание аккаунта пользователем"""

    model = PortUser
    form_class = PortUserCreationForm
    success_message = 'A link to confirm registration has been sent to your mailing address.'
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Отправка на почту письма с подтверждением"""
        user = form.save(commit=False)
        user.is_active = False
        url_confirm = self.request.build_absolute_uri(
            reverse_lazy('confirm_user', args=(user.email, user.confirm_user)))
        message = f'To confirm follow the link: {url_confirm}'
        send_mail('Proof of mailing address', message, '_', [user.email])
        user.save()
        return super(SignUp, self).form_valid(form)


def confirm_user(request, email, uuid):
    """Подтверждение регистрации на почте"""
    user = get_object_or_404(PortUser, email=email)

    if user.is_active:
        messages.info(request, 'Your account is already verified')

    elif str(user.confirm_user) == uuid:  #Если пользователь подтвердил регистрацию, ставим статус True и добавляем-
        # пробную подписку ( 'trial access' )
        user.is_active = True
        user.save()
        Subscrip(user).create_trial_access()
        messages.info(request, 'User created successfully, you can login')

    return redirect('login')


class PortChangePassword(SuccessMessageMixin, PasswordChangeView):
    """Изменение пароля"""
    success_message = 'Password change successful'
    success_url = reverse_lazy('account')


@login_required
def get_subscribe(request, type_sub):
    """Оформление подписки"""

    user = PortUser.objects.get(email=request.user)
    subs = Subscrip(user)
    if request.method == 'POST':
        data_post = request.POST
        subs.create_subscribe(data_post, type_sub)
        return redirect('account')

    if type_sub == '1 MONTH':
        cargos = subs.get_cargo_not_user['1_month']

    elif type_sub == '6 MONTHS':
        cargos = subs.get_cargo_not_user['6_months']

    context = {'cargos': cargos}
    return render(request, 'account/to_subscribe.html', context)

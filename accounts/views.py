
from django.shortcuts import render, redirect
from django.views.generic import *
# from .forms import UserCreationForm, LoginForm
# from django.contrib.auth.views import LoginView, LogoutView

# 以下のimportはコピペ
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
# from django.shortcuts import redirect
from django.template.loader import render_to_string
# from django.views import generic
from .forms import (
    LoginForm, UserCreateForm,
)

User = get_user_model()


# Create your views here.
"""
class Register(View):
    template_name = 'accounts/register.html'
    params = {
        'form': UserCreateForm(),
    }

    def get(self, request):
        return render(request, self.template_name, self.params)

    def post(self, request):
        return render(request, self.template_name, self.params)
"""


class Top(TemplateView):
    template_name = 'accounts/top.html'


class Login(LoginView):
    """ログインページ"""
    form_class = LoginForm
    template_name = 'accounts/login.html'


class Logout(LogoutView):
    """ログアウトページ"""
    template_name = 'accounts/logout.html'


class UserCreate(CreateView):
    """ユーザー仮登録"""
    template_name = 'accounts/user_create.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': self.request.scheme,
            'domain': domain,
            'token': dumps(user.pk),
            'user': user,
        }

        subject = render_to_string('accounts/mail_template/create/subject.txt', context)
        message = render_to_string('accounts/mail_template/create/message.txt', context)

        user.email_user(subject, message, 'tkmn@tkmail.com')
        return redirect('accounts:user_create_done')


class UserCreateDone(TemplateView):
    """ユーザー仮登録したよ"""
    template_name = 'accounts/user_create_done.html'


class UserCreateComplete(TemplateView):
    """メール内URLアクセス後のユーザー本登録"""
    template_name = 'accounts/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

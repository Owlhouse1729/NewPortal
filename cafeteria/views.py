from django.shortcuts import render, redirect
from django.views.generic import *
from django.utils import timezone
from .models import Seat
from accounts.models import User


class Top(TemplateView):
    template_name = 'cafeteria/top.html'


class Reserve(View):
    template_name = 'cafeteria/reserve.html'
    reserve_limit_first = 20
    reserve_limit_second = 20

    def get(self, request):
        reserve_count_first = Seat.objects.filter(half=1).count()
        reserve_count_second = Seat.objects.filter(half=2).count()
        user_pk = self.request.user.pk
        user = User.objects.get(pk=user_pk)
        am_reserving = '予約はありません'
        if Seat.objects.filter(user=user).count():
            am_reserving = 'すでに予約しています'
        params = {
            'reserve_count_first': reserve_count_first,
            'reserve_limit_first': self.reserve_limit_first,
            'reserve_count_second': reserve_count_second,
            'reserve_limit_second': self.reserve_limit_second,
            'ticket': user.cafeteria_ticket,
            'am_reserving': am_reserving
        }
        return render(request, self.template_name, params)

    def post(self, request):
        print(request.POST)
        reserve_count_first = Seat.objects.filter(half=1).count()
        reserve_count_second = Seat.objects.filter(half=2).count()
        user_pk = self.request.user.pk
        user = User.objects.get(pk=user_pk)
        if 'first' in request.POST:
            if (reserve_count_first <= self.reserve_limit_first) and \
                    (user.cafeteria_ticket > 0) and \
                    not (Seat.objects.filter(user=user).count()):
                Seat.objects.create(half=1, user=user)
                user.cafeteria_ticket -= 1
                user.save()
        elif 'second' in request.POST:
            if (reserve_count_second <= self.reserve_limit_second) and \
                    (user.cafeteria_ticket > 0) and \
                    not (Seat.objects.filter(user=user).count()):
                Seat.objects.create(half=2, user=user)
                user.cafeteria_ticket -= 1
                user.save()
        else:
            pass
        return redirect('cafeteria:reserve')


class Check(View):
    template_name = 'cafeteria/check.html'

    def get(self, request):
        user_pk = self.request.user.pk
        user = User.objects.get(pk=user_pk)
        am_reserving = '予約はありません'
        seat_id = '-'
        if Seat.objects.filter(user=user).count():
            am_reserving = '予約があります'
            seat_id = Seat.objects.all().count() + 1
        params = {
            'param': '予約param',
            'am_reserving': am_reserving,
            'seat_id': seat_id,
        }
        if Seat.objects.filter(user=user):
            params['half'] = Seat.objects.get(user=user).half
        return render(request, self.template_name, params)

    def post(self, request):
        user_pk = self.request.user.pk
        user = User.objects.get(pk=user_pk)
        Seat.objects.filter(user=user).delete()
        user.cafeteria_ticket += 1
        user.save()
        return redirect('cafeteria:check')

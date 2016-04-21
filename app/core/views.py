# -*- coding: utf-8 -*-
import datetime

import jwt
import redis
from django.conf import settings
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from core.models import AdsModel

r = redis.StrictRedis(host='localhost', port=6379, db=0)

"""
#
# HomePageView
#
"""


class HomePageView(ListView):
    template_name = 'core/list.html'
    model = AdsModel
    ordering = ['-created']


"""
#
# AdsDetailView
#
"""
def create_key(user, obj, session_key, ip):
    payload = {
        'user_id': user.id,
        'obj_id': obj.id,
        'session_key': session_key,
        'ip': ip
    }
    key = jwt.encode(payload, settings.SECRET_KEY)
    k = "sorter_" + str(obj.id) + "_" + key.decode('unicode_escape')
    return k

def parse_key(key, obj):
    key = key.replace('sorter_' + str(obj.id) + '_', '')
    return jwt.decode(key, settings.SECRET_KEY)

"""
#
# Можем проверять по всем данным, запустить celery что очищал редис и забивал в базу и т.п. Дорабывать есть куда
#
"""

class AdsDetailView(HitCountDetailView):
    template_name = 'core/detail.html'
    model = AdsModel
    count_hit = True
    counter_views = {}

    def counter(self, *args, **kwargs):

        # формируем значения ключа для редис
        session_key = self.request.session.session_key
        ip = self.request.META['REMOTE_ADDR']
        obj = self.get_object()

        viewed = True

        # создаем ключ
        key = create_key(self.request.user, obj, session_key, ip)

        # если нету записываем в редис
        if not r.get(key):
            viewed = False
            r.set(key, str(obj.id))

        parser_key = parse_key(key, obj)

        print(key)
        print(parser_key)

        self.counter_views['counter'] = len(r.keys('sorter_1_*'))
        self.counter_views['viewed'] = viewed


    def dispatch(self, *args, **kwargs):

        self.counter(*args, **kwargs)

        return super(AdsDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AdsDetailView, self).get_context_data(**kwargs)

        context['counter_views'] = self.counter_views
        return context

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from hitcount.views import HitCountDetailView

from core.models import AdsModel

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


class AdsDetailView(HitCountDetailView):
    template_name = 'core/detail.html'
    model = AdsModel
    count_hit = True

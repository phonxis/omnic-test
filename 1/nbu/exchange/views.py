# -*- coding: utf-8 -*-

from datetime import datetime

import requests
from rest_framework import viewsets, generics
from rest_framework.response import Response

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.db import IntegrityError

from .models import Exchange
from .serializers import ExchangeSerializer

# Create your views here.


def index(request):
	r = requests.get("https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json")
	for data in r.json():
		try:
			Exchange.objects.create(
				r030=data["r030"],
				cc=data["cc"],
				txt=data["txt"],
				rate=data["rate"],
				exchangedate=datetime.strptime(data["exchangedate"], '%d.%m.%Y')
			)
		except IntegrityError:
			return HttpResponseBadRequest()

	return HttpResponse()


class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.today()
    serializer_class = ExchangeSerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = ExchangeSerializer

    def get_queryset(self):
        queryset = Exchange.objects.all()
        cc = self.request.query_params.get('cc', None)
        if cc is not None:
            queryset = queryset.filter(cc=cc)
        return queryset

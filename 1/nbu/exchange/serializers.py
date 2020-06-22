from rest_framework import serializers

from .models import Exchange

# Serializers define the API representation.


class ExchangeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exchange
        fields = ['cc', 'exchangedate', 'rate', 'r030', 'txt']

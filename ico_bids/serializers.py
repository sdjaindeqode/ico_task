from rest_framework import serializers
from ico_bids.models import Token, Bid


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
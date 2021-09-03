from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import TokenSerializer, BidSerializer
from .models import Token, Bid
# Create your views here.

class TokenView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

class TokenDetailView(RetrieveAPIView):
    permission_classes = [AllowAny,]
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

class BidDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = BidSerializer

    def get_queryset(self):
        return (
            Bid.objects
            .filter(user=self.request.user)
        )

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        request.data['user'] = self.request.user.id
        request.data.pop('token')
        return super().update(request, *args, **kwargs)


class CreateBidView(CreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = BidSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        try:
            bid = (
                Bid.objects
                .get(
                    user=self.request.user,
                    token=validated_data['token'],
                )
            )
        except Bid.DoesNotExist:
            bid = None

        if bid:
            serializer.instance = bid
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SuccessBidView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BidSerializer
    queryset = Bid.objects.filter(status=Bid.STATUS[0][0])


class FailedBidView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = BidSerializer
    queryset = Bid.objects.filter(status=Bid.STATUS[1][0])
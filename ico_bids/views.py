from datetime import datetime
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
from rest_framework.renderers import TemplateHTMLRenderer
from .serializers import TokenSerializer, BidSerializer
from .models import Token, Bid
# Create your views here.

class TokenView(ListAPIView):
    """
    This view is used to request list of token available for offering.
    Methods: GET
    Permissions: AllowAny
    Endpoint: 'api/v1/token/'
    """
    permission_classes = (AllowAny,)
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

class TokenDetailView(RetrieveAPIView):
    """
    This view is used to request a specific token's detail.
    Methods: GET
    Permissions: AllowAny
    Endpoint: 'api/v1/token/<int:pk>'
    """
    permission_classes = [AllowAny,]
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

class BidDetailView(RetrieveUpdateDestroyAPIView):
    """
    This view is used to retreive, update and delete the request bid.
    Methods: GET, PUT, DELETE
    Permissions: IsAuthenticated
    Endpoint: 'api/v1/bid/<int:pk>'
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = BidSerializer

    def get_queryset(self):
        return (
            Bid.objects
            .filter(user=self.request.user)
        )

    def update(self, request, *args, **kwargs):
        """
        Called by HTTP PUT method used to update the bid.
        Authorization header should be passed to request.
        Example - Authorization : Token <user-token obtained while login>
        Args:
            number_of_token: number of token needed by user.
            bid_price: bidding price for the token.

        Returns:
            Returns the newly updated bid details
        """
        kwargs['partial'] = True
        request.data['user'] = self.request.user.id
        if request.data.get('token'):
            request.data.pop('token')
        return super().update(request, *args, **kwargs)


class CreateBidView(CreateAPIView):
    """
    This view is used to create a new bid.
    Methods: POST
    Permissions: IsAuthenticated
    Endpoint: 'api/v1/bid/'
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = BidSerializer

    def create(self, request, *args, **kwargs):
        """
        Called by HTTP POST method used to create a new bid.
        Authorization header should be passed to request.
        Example - Authorization : Token <user-token obtained while login>
        Args:
            token: token_id on which user want to bid.
            number_of_token: number of token needed by user.
            bid_price: bidding price for the token.

        Returns:
            Returns the newly created bid details
            If the user already bid on the same token previously
            then, that will be returned.
        """
        data = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        token = validated_data['token']
        curr_time = datetime.now().time()
        if not token.start_time < curr_time < token.end_time:
            response = {
                'message': 'Please bid during bidding timing of the token'
            }
            return Response(
                response, status=status.HTTP_403_FORBIDDEN
            )
        bid = Bid.objects.filter(user=self.request.user, token=token)
        if bid:
            response = {
                'message': 'You have already created a bid for the token. Please update it.'
            }
            return Response(
                response, status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class SuccessBidView(ListAPIView):
    """
    This view is used to return all the successfull bids.
    Methods: GET
    Permissions: AllowAny
    Endpoint: 'api/v1/bid/success'
    """
    permission_classes = (AllowAny,)
    serializer_class = BidSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        queryset = Bid.objects.filter(status=Bid.STATUS[0][0])
        return Response({'queryset': queryset}, template_name='successfull_bid.html') 



class FailedBidView(ListAPIView):
    """
    This view is used to return all the failed bids.
    Methods: GET
    Permissions: AllowAny
    Endpoint: 'api/v1/bid/failed'
    """
    permission_classes = (AllowAny,)
    serializer_class = BidSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        queryset = Bid.objects.filter(status=Bid.STATUS[1][0])
        return Response({'queryset': queryset}, template_name='failed_bid.html') 
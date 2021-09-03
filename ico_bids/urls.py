from django.contrib import admin
from django.urls import path
from .views import (
    TokenView,
    TokenDetailView,
    CreateBidView,
    BidDetailView,
    SuccessBidView,
    FailedBidView,
)

urlpatterns = [
    path('token/', (TokenView.as_view()), name='token'),
    path('token/<int:pk>/', (TokenDetailView.as_view()), name='token-detail'),
    path('bid/', (CreateBidView.as_view()), name='create-bid'),
    path('bid/<int:pk>/', (BidDetailView.as_view()), name='bid-detail'),
    path('bid/success/', (SuccessBidView.as_view()), name='successfull-bid'),
    path('bid/failed/', (FailedBidView.as_view()), name='failed-bid'),
]

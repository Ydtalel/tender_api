from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TenderViewSet, BidViewSet, ping

tender_router = SimpleRouter(
    trailing_slash=False)  # убрать trailing_slash=False
# что бы маршруты работали с / на конце
tender_router.register(r'tenders', TenderViewSet)

bid_router = SimpleRouter(trailing_slash=False)  # убрать trailing_slash=False
# что бы маршруты работали с / на конце
bid_router.register(r'bids', BidViewSet)

urlpatterns = [
    path('ping', ping, name='ping'),
    path('', include(tender_router.urls)),
    path('', include(bid_router.urls)),
]

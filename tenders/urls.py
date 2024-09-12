from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import TenderViewSet, BidViewSet, ping

router = SimpleRouter()
router.register(r'tenders', TenderViewSet)

bid_router = SimpleRouter()
bid_router.register(r'bids', BidViewSet)

urlpatterns = [
    path('ping', ping, name='ping'),
    path('', include(router.urls)),
    path('', include(bid_router.urls)),
]
# урлы не работают без / на конце, нужно пофиксить

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from matches.views import MatchViewSet
from members.views import MemberViewSet, AuthToken

r = routers.DefaultRouter()
r.register(r'members', MemberViewSet)
r.register(r'matches', MatchViewSet)

urlpatterns = [
    path('api/', include(r.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', AuthToken.as_view()),
]

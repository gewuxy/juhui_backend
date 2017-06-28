# -*- coding: UTF-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
# from apps import index

from rest_framework import permissions, routers, serializers, viewsets
from oauth2_provider.contrib.rest_framework import (
    TokenHasReadWriteScope,
    TokenHasScope
)
from django.contrib.auth.models import User, Group
admin.autodiscover()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name", )


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    # url(r'^$', index, name='index'),
    url(r'^', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/account/', include('apps.account.urls', namespace='account')),
    url(r'^api/wine/', include('apps.wine.urls', namespace='wine'))
]

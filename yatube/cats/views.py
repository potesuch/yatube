from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.throttling import ScopedRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from .models import Cat, User, Achievement
from .serializers import (CatSerializer, CatListSerializer,
                          UserSerializer, AchievementSerializer)
from .permissions import OwnerOrReadOnly, ReadOnly
from .throttling import WorkingHoursRateThrottle


class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    #serializer_class = CatSerializer
    permission_classes = (OwnerOrReadOnly,)
    throttle_classes = (WorkingHoursRateThrottle, ScopedRateThrottle)
    #throttle_scope = 'low_request'
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('color', 'birth_year')

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        cats = Cat.objects.filter(color='White')[:5]
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action == 'list':
            return CatListSerializer
        return CatSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class AchievementViewSet(viewsets.ModelViewSet):
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass


class CatLightViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class TestViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Cat.objects.all()
        cat = get_object_or_404(queryset, pk=pk)
        serializer = CatSerializer(cat)
        return Response(serializer.data)

    def list(self, request):
        queryset = Cat.objects.all()
        serializer = CatSerializer(queryset, many=True)
        return Response(serializer.data)

"""
Viewsets (highly customizable).
"""
from rest_framework.viewsets import *
from my_apps.rest.models import Temp1, Temp1Serializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import renderers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django_filters.rest_framework import DjangoFilterBackend


# class ClassViewset(ViewSet):
#     def list(self, request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


# class ClassViewset(ReadOnlyModelViewSet):
#     # `list` and `retrieve`
#     queryset = Temp1.objects.all()
#     serializer_class = Temp1Serializer


class ClassViewset(ModelViewSet):
    # `list`, `create`, `retrieve`, `update` and `destroy`
    queryset = Temp1.objects.all()
    serializer_class = Temp1Serializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'description']

    def get_view_description(self, html=False):
        return "My description."

    ##########################################################################

    # extra actions - detail
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer], name='Render Title', url_path='title')
    def render_title(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.title)

    @action(detail=False, name='Render All', url_path='all')
    def render_all(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    ###########################################################################

    # extra actions - single route with multiple methods
    @action(detail=True, methods=["post"], name="Single Route")
    def single_route(self, request, pk=None):
        return Response({'message': 'I POST'})

    @single_route.mapping.get
    def single_route_get(self, request, pk=None):
        return Response({'message': 'I GET'})

"""
Generic Views (for models).
"""
from my_apps.rest.models import TempModel, TempModelSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 5


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 5


# generics uses mixins (this is the best view so far)
class ClassGenericsView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TempModel.objects.all()
    serializer_class = TempModelSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'description', 'created_at']
    ordering_fields = '__all__'
    pagination_class = CustomLimitOffsetPagination

    # no need to mention the below methods unless there is a custom logic
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClassGenericsPkView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TempModel.objects.all()
    serializer_class = TempModelSerializer

    # no need to mention the below methods unless there is a custom logic
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        # custom logic - to manipulate data before update
        data_copy = request.data.copy()
        data_copy['description'] = 'fixed desc while put'
        request._full_data = data_copy
        # custom logic - end
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

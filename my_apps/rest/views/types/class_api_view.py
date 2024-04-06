"""
Class based View.
"""
from rest_framework.views import APIView
from my_apps.rest.models import Temp2, Temp2Serializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.versioning import AcceptHeaderVersioning


class CustomUserRateThrottle(UserRateThrottle):
    rate = '5/min'


class CustomAcceptHeaderVersioning(AcceptHeaderVersioning):
    default_version = '1.0'
    allowed_versions = ['1.0', '2.0']


class ClassApiView(APIView):
    queryset = Temp2.objects.all()
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]
    versioning_class = CustomAcceptHeaderVersioning

    def get(self, request, format=None):
        queryset = Temp2.objects.all()
        serializer = Temp2Serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = Temp2Serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassApiPkView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Temp2.objects.get(pk=pk)
        except Temp2.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = Temp2Serializer(queryset, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = Temp2Serializer(queryset, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

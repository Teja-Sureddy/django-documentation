"""
Function based View.
"""

from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from my_apps.rest.models import Temp1, Temp1Serializer
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def function_api_view(request, format=None):
    if request.method == 'GET':
        queryset = Temp1.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        filtered_queryset = SearchFilter().filter_queryset(request, queryset, view=function_api_view)
        result_page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = Temp1Serializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = Temp1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def function_api_pk_view(request, pk, format=None):
    try:
        queryset = Temp1.objects.get(pk=pk)
    except Temp1.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Temp1Serializer(queryset)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Temp1Serializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

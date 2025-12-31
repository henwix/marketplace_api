from collections.abc import Iterable

from rest_framework import status
from rest_framework.pagination import BasePagination
from rest_framework.serializers import Serializer
from rest_framework.views import Response


class PaginationViewMixin:
    def paginate(
        self,
        queryset: Iterable,
        paginator: type[BasePagination],
        serializer: type[Serializer],
    ) -> Response:
        queryset = self.filter_queryset(queryset=queryset)
        paginator = paginator()

        page = paginator.paginate_queryset(queryset=queryset, request=self.request, view=self)
        if page is not None:
            serializer = serializer(page, many=True, context=self.get_serializer_context())
            return paginator.get_paginated_response(data=serializer.data)
        serializer = serializer(queryset, many=True, context=self.get_serializer_context())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LazyAuthViewMixin:
    def perform_authentication(self, request): ...

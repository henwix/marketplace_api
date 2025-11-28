from logging import Logger

import orjson
import punq
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.views import Response
from rest_framework.viewsets import GenericViewSet

from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.common.exceptions import ServiceException
from src.apps.users.docs.schema_decorators import extend_user_viewset_schema
from src.apps.users.models import User
from src.apps.users.permissions import UserPermission
from src.apps.users.use_cases.create import CreateUserUseCase
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from src.project.containers import get_container


@extend_user_viewset_schema
class UserViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = User.objects.all()
    permission_classes = [UserPermission]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.container: punq.Container = get_container()
        self.logger: Logger = self.container.resolve(Logger)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve']:
            return UserSerializer
        if self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        if self.action == 'set_password':
            return PasswordUserSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: CreateUserUseCase = self.container.resolve(CreateUserUseCase)

        try:
            result = use_case.execute(data=serializer.validated_data)
            return Response(data=self.get_serializer(result).data, status=status.HTTP_201_CREATED)
        except ServiceException as error:
            self.logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    @action(['post'], detail=False)
    def set_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: SetPasswordUserUseCase = self.container.resolve(SetPasswordUserUseCase)

        result = use_case.execute(user=request.user, password=serializer.validated_data['new_password'])
        return Response(data=result, status=status.HTTP_200_OK)

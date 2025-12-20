from logging import Logger

import orjson
from punq import Container
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response

from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.common.exceptions import ServiceException
from src.apps.users.converters import user_to_entity
from src.apps.users.docs.schema_decorators import (
    extend_set_password_user_view_schema,
    extend_user_view_schema,
)
from src.apps.users.permissions import CreateOrIsAuthenticated
from src.apps.users.use_cases.create import CreateUserUseCase
from src.apps.users.use_cases.delete import DeleteUserUseCase
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from src.apps.users.use_cases.update import UpdateUserUseCase
from src.project.containers import get_container


@extend_user_view_schema()
class UserView(APIView):
    permission_classes = [CreateOrIsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container: Container = get_container()
        self.logger: Logger = self.container.resolve(Logger)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: CreateUserUseCase = self.container.resolve(CreateUserUseCase)

        try:
            user = use_case.execute(data=serializer.validated_data)
            return Response(
                data=UserSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )
        except ServiceException as error:
            self.logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def get(self, request):
        user = request.user
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    def update(self, request, partial: bool):
        serializer = UpdateUserSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateUserUseCase = self.container.resolve(UpdateUserUseCase)

        try:
            user = use_case.execute(
                user=user_to_entity(dto=request.user),
                data=serializer.validated_data,
            )
            return Response(
                data=UpdateUserSerializer(user).data,
                status=status.HTTP_200_OK,
            )
        except ServiceException as error:
            self.logger.error(msg=error.message, extra={'log_meta': orjson.dumps(error).decode()})
            return Response(data=error.response(), status=error.status_code)

    def put(self, request):
        return self.update(request=request, partial=False)

    def patch(self, request):
        return self.update(request=request, partial=True)

    def delete(self, request):
        use_case: DeleteUserUseCase = self.container.resolve(DeleteUserUseCase)
        use_case.execute(user_id=request.user.pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_set_password_user_view_schema()
class SetPasswordUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        container: Container = get_container()
        serializer = PasswordUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: SetPasswordUserUseCase = container.resolve(SetPasswordUserUseCase)

        result = use_case.execute(user=user_to_entity(request.user), password=serializer.validated_data['new_password'])
        return Response(data=result, status=status.HTTP_200_OK)

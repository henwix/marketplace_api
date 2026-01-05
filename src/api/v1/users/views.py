from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from src.api.v1.users.openapi.decorators import (
    extend_set_password_user_view_schema,
    extend_user_view_schema,
)
from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.users.commands import (
    CreateUserCommand,
    DeleteUserCommand,
    GetUserCommand,
    SetPasswordUserCommand,
    UpdateUserCommand,
)
from src.apps.users.use_cases.create import CreateUserUseCase
from src.apps.users.use_cases.delete import DeleteUserUseCase
from src.apps.users.use_cases.get import GetUserUseCase
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from src.apps.users.use_cases.update import UpdateUserUseCase
from src.project.containers import resolve_depends


@extend_user_view_schema()
class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: CreateUserUseCase = resolve_depends(CreateUserUseCase)
        command = CreateUserCommand(data=serializer.validated_data)
        user = use_case.execute(command=command)
        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        use_case: GetUserUseCase = resolve_depends(GetUserUseCase)
        command = GetUserCommand(user_id=request.user.id)
        user = use_case.execute(command=command)
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    def _update(self, request: Request, partial: bool) -> Response:
        serializer = UpdateUserSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateUserUseCase = resolve_depends(UpdateUserUseCase)
        command = UpdateUserCommand(user_id=request.user.id, data=serializer.validated_data)
        user = use_case.execute(command=command)
        return Response(data=UpdateUserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        return self._update(request=request, partial=False)

    def patch(self, request: Request) -> Response:
        return self._update(request=request, partial=True)

    def delete(self, request: Request) -> Response:
        use_case: DeleteUserUseCase = resolve_depends(DeleteUserUseCase)
        command = DeleteUserCommand(user_id=request.user.id)
        use_case.execute(command=command)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_set_password_user_view_schema()
class SetPasswordUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = PasswordUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: SetPasswordUserUseCase = resolve_depends(SetPasswordUserUseCase)
        command = SetPasswordUserCommand(user_id=request.user.id, password=serializer.validated_data['new_password'])
        result = use_case.execute(command=command)
        return Response(data=result, status=status.HTTP_200_OK)

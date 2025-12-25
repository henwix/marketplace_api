from punq import Container
from rest_framework import status
from rest_framework.request import Request
from rest_framework.views import APIView, Response

from src.api.v1.users.serializers import PasswordUserSerializer, UpdateUserSerializer, UserSerializer
from src.apps.users.docs.schema_decorators import (
    extend_set_password_user_view_schema,
    extend_user_view_schema,
)
from src.apps.users.use_cases.create import CreateUserUseCase
from src.apps.users.use_cases.delete import DeleteUserUseCase
from src.apps.users.use_cases.get import GetUserUseCase
from src.apps.users.use_cases.set_password import SetPasswordUserUseCase
from src.apps.users.use_cases.update import UpdateUserUseCase
from src.project.containers import get_container


@extend_user_view_schema()
class UserView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container: Container = get_container()

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        use_case: CreateUserUseCase = self.container.resolve(CreateUserUseCase)
        user = use_case.execute(data=serializer.validated_data)
        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        use_case: GetUserUseCase = self.container.resolve(GetUserUseCase)
        user = use_case.execute(user_id=request.user.id)
        return Response(data=UserSerializer(user).data, status=status.HTTP_200_OK)

    def update(self, request: Request, partial: bool) -> Response:
        serializer = UpdateUserSerializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        use_case: UpdateUserUseCase = self.container.resolve(UpdateUserUseCase)
        user = use_case.execute(user_id=request.user.id, data=serializer.validated_data)
        return Response(data=UpdateUserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request: Request) -> Response:
        return self.update(request=request, partial=False)

    def patch(self, request: Request) -> Response:
        return self.update(request=request, partial=True)

    def delete(self, request: Request) -> Response:
        use_case: DeleteUserUseCase = self.container.resolve(DeleteUserUseCase)
        use_case.execute(user_id=request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_set_password_user_view_schema()
class SetPasswordUserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = PasswordUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        container: Container = get_container()
        use_case: SetPasswordUserUseCase = container.resolve(SetPasswordUserUseCase)
        result = use_case.execute(user_id=request.user.id, password=serializer.validated_data['new_password'])
        return Response(data=result, status=status.HTTP_200_OK)

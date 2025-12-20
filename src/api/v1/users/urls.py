from django.urls import path

from src.api.v1.users.views import SetPasswordUserView, UserView

app_name = 'users'


urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('users/set_password/', SetPasswordUserView.as_view(), name='users-set-password'),
]

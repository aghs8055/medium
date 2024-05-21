from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from users.views import signup, login, logout

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
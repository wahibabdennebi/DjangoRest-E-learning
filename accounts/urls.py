from django.urls import path
from .views import  ListUsers, ProfileUser,ProfileAPI, UpdateUserView,LogoutAPIView
urlpatterns = [
path('users/', ListUsers.as_view(), name='auth_list_users'),
# path('detail/<int:pk>/', DetailUserView.as_view(), name='auth_detail_users'),
# path('views/<int:pk>/', UserView.ViewSet()),
path('profile/',ProfileUser.as_view()),
path('users/<user_id>/', ProfileAPI.as_view()),
path('updateProfile/<int:pk>/', UpdateUserView.as_view(), name='update_user'),
path('logout/', LogoutAPIView.as_view(), name="logout"),
]
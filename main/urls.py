from django.urls import path
from .views import index, other_page, OLXLoginView, profile, OLXLogoutView, \
    ChangeUserView, UserPasswordChangeView, RegisterUserView, RegisterDoneView, \
    DeleteUserView, user_activate, profile_detail_elonlar, profile_elon_create, \
    profile_elon_change,profile_elon_delete

urlpatterns = [
    path('', index, name='index'),
    path('<str:page>/', other_page, name='other'),
    path('accounts/profile/update/<int:pk>/', profile_elon_change, name='profile_elon_update'),
    path('accounts/profile/delete/<int:pk>/', profile_elon_delete, name='profile_elon_delete'),
    path('accounts/profile/change/', ChangeUserView.as_view(), name='user_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='user_delete'),
    path('accounts/profile/add/', profile_elon_create, name='profile_elon_create'),
    path('accounts/profile/<int:pk>/', profile_detail_elonlar, name='profile_detail_elonlar'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/login/', OLXLoginView.as_view(), name='login'),
    path('accounts/logout/', OLXLogoutView.as_view(), name='logout'),
]
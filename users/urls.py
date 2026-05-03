from django.urls import path
from . import views


app_name = 'users'


urlpatterns = [
    path('list/', views.UserList.as_view(), name='user_list'),
    path('<int:user_id>/', views.UserDetail.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('edit-profile/', views.ProfileEditView.as_view(),
         name='profile_edit'),
    path('change-password/', views.PasswordChangeView.as_view(),
         name='password_change'),
    path('logout/', views.MyLogoutView.as_view(), name='logout')
]

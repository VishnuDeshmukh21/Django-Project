from django.urls import path,include
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns=[
  path("register",user_views.register_user,name='register'),
  path("login",user_views.UserLoginView.as_view( template_name='users/login.html'),name='login'),
  path("logout",auth_views.LogoutView.as_view( template_name='users/logout.html'),name='logout'),
  path("profile/view",user_views.view_profile,name='profile_view'),
  path("profile/edit",user_views.edit_profile,name='profile_edit'),

]
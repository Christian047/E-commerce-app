from django.urls import path
from . import views

   
   
urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    ]
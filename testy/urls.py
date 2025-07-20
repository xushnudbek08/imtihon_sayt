from django.urls import path
from . import views



urlpatterns = [
    path('',views.firstpage, name='firstpage'),
    
    path('home/', views.home, name='home'),
    path('test/', views.test, name='test'),
   
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_step_one, name='register_step_one'),
    path('verify-email/', views.verify_email_code, name='verify_email_code')
   
]
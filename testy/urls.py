from django.urls import path
from . import views



urlpatterns = [
    path('', views.redirect_user, name='redirect_user'),
    path('firstpage/', views.firstpage, name='firstpage'),
    path('home/', views.home, name='home'),
     path('news/', views.NewsListView, name='news_list'),
   path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_step_one, name='register'),
    path('verify-email/', views.verify_email_code, name='email'),
    path('admin-panel/yuklash/', views.upload_excel, name='upload_excel'),
    path('testlar/', views.category_list, name='category_list'),
    path('testlar/<int:category_id>/', views.start_test, name='start'),
    path('statistika/', views.profile_stats, name='profile_stats')
 

   
]
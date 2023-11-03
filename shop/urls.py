from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home_page'),
    path('admin/returns/<int:return_id>/confirm/', views.confirm_return, name='confirm_return'),
    path('login/', auth_views.LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name=''), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('purchase/<int:product_id>/', views.create_order, name='create_order'),
    path('return_item/<int:order_item_id>/', views.return_item, name='return_item'),
]

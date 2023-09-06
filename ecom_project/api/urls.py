from django.urls import path, include
from . import views



app_name = 'api'  # Add this line to define the namespace

urlpatterns = [
    
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path('product/', views.product, name='product'),
     path('create-review/', views.create_review, name='create_review'),
    path('product-list/', views.product_list, name='product_list'),

] 


from django.contrib import admin
from django.urls import path, include
from api import views  # Import your views

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', views.home_page, name='home_page'),  # Add this line to map the root URL to the home_page view
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path('register/', views.register, name='register'),
    # path('login/', views.login_user, name='login_user'),
]

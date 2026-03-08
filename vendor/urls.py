from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import VendorLoginForm

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('add-vendor/', views.add_vendor, name='add_vendor'),

    # Authentication
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html',
            authentication_form=VendorLoginForm,
        ),
        name='login',
    ),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

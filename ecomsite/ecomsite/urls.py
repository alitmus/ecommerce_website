"""
URL configuration for ecomsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users.views import register,profilepage,AddressCreateView,AddressUpdateView,edit_user ,AddressDeleteView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',RedirectView.as_view(url='shop/')),
    path('shop/',include('shop.urls')),
    path('register/',register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/',profilepage,name='profile'),
    path('address_form/',AddressCreateView.as_view(),name='address_form'),
    path('address_update/<int:pk>/',AddressUpdateView.as_view(),name='address_update'),
    path('address_delete/<int:pk>/',AddressDeleteView.as_view(),name='address_delete'),
    path('edit_user/',edit_user,name='edit_user'),
]





urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
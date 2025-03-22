"""
URL configuration for d09 project.

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
# d09/urls.py
from django.contrib import admin
from django.urls import path
from account.views import account_view, login_ajax, logout_ajax

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', account_view, name='account_home'),
    path('account/login_ajax/', login_ajax, name='login_ajax'),
    path('account/logout_ajax/', logout_ajax, name='logout_ajax'),
]

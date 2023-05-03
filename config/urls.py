"""
URL configuration for config project.

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
from django.urls import path
import app.views as views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('index/', views.index),
    path('', views.index),
    path("noodle_worldcup/", views.noodle_worldcup),
    path("chicken_worldcup/", views.chicken_worldcup),
    path("snack_worldcup/", views.snack_worldcup),
    path("food_worldcup/", views.food_worldcup),  

    path('signup/', views.signup),
    path('signin/', views.signin),
    path('signout/', views.signout),

    path('email_check/', views.email_check), 

    path('app/write/', views.write),
    path('app/list/', views.list),
    path('app/detail/<int:id>/', views.detail),
    path('app/update/<int:id>/', views.update),

    path('app/notice/', views.notice),
    path('app/write2/', views.write2),
    path('app/detail2/<int:id>/', views.detail2),
    path('app/update2/<int:id>/', views.update2),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
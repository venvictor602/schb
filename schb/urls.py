"""
URL configuration for schb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from document_app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('oil-producer/', document_view, name='document_view'),
    path('upper-oil/', upper_oil, name='upper_oil'),
    path('both-oil/', both_oil, name='both_oil'),
    path('water-injector-1/', water_injector_1, name='water_injector_1'),
    path('water-injector-2/', water_injector_2, name='water_injector_2'),
    path('lower-suspension-fibre/', lower_suspension_fibre, name='lower_suspension_fibre'),
    path('upper-lower-fibre/', upper_lower_fibre, name='upper_lower_fibre'),
    path('', index, name='index'),
    # path('excel-to-word/', excel_to_word, name='excel_to_word'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

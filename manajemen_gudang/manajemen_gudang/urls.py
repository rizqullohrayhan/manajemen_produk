from django.contrib import admin
from django.urls import path, include

from produk import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("produk.urls")),
    path('fetch-api/', views.fetch_and_save_data),
]

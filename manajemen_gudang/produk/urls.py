from django.urls import path

from . import views

app_name = "produk"

urlpatterns = [
    path("", views.ProdukListView.as_view(), name="list"),
    path("create/", views.ProdukCreateView.as_view(), name="create"),
    path("update/<int:pk>", views.ProdukUpdateView.as_view(), name="update"),
    path("delete/<int:pk>", views.ProdukDeleteView.as_view(), name="delete"),
]
import requests
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from .models import Produk, Kategori, Status
from .serializers import ProdukSerializer

from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


def fetch_and_save_data(request):
    url = "https://recruitment.fastprint.co.id/tes/api_tes_programmer"
    payload = {
        "username": "tesprogrammer110125C21",
        "password": "4ac0087b411a38bad7c428dd1add9a8b"
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        api_data = response.json()

        # Menyimpan data ke database
        for item in api_data['data']:
            kategori_object, _ = Kategori.objects.get_or_create(nama_kategori=item['kategori'])
            status_object, _ = Status.objects.get_or_create(nama_status=item['status'])
            produk_data = {
                "nama_produk": item['nama_produk'],
                "harga": int(item['harga']),
                "kategori": kategori_object,
                "status": status_object
            }
            serializer = ProdukSerializer(data=produk_data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        return JsonResponse({"message": "Data berhasil disimpan ke database."})

    else:
        return JsonResponse({
            "error": f"Gagal memanggil API: {response.status_code}",
            "details": response.text
        }, status=response.status_code)


class ProdukListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "produk/list.html"

    def get_queryset(self):
        status_bisa_dijual = Status.objects.get(nama_status="bisa dijual")
        return Produk.objects.filter(status=status_bisa_dijual)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response({'produks': queryset})


class ProdukCreateView(generics.CreateAPIView):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "produk/create.html"

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class()
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Produk berhasil ditambahkan.")
            return HttpResponseRedirect(reverse("produk:list"))
        return Response({'serializer': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProdukUpdateView(generics.UpdateAPIView):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "produk/update.html"

    def get(self, request, *args, **kwargs):
        produk = get_object_or_404(Produk, pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance=produk)
        return Response({'serializer': serializer})

    def post(self, request, *args, **kwargs):
        produk = get_object_or_404(Produk, pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance=produk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Produk berhasil diedit.")
            return HttpResponseRedirect(reverse("produk:list"))
        return Response({'serializer': serializer, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProdukDeleteView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'DELETE':
            return self.delete(request, *args, **kwargs)
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    def delete(self, request, *args, **kwargs):
        produk = get_object_or_404(Produk, pk=kwargs.get('pk'))
        produk.delete()
        return JsonResponse({'message': 'Produk berhasil dihapus'}, status=200)
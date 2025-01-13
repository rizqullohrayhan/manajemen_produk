from rest_framework import serializers
from .models import Produk, Kategori, Status


class ProdukSerializer(serializers.ModelSerializer):
    kategori = serializers.SlugRelatedField(
        queryset=Kategori.objects.all(),
        slug_field='nama_kategori'
    )
    status = serializers.SlugRelatedField(
        queryset=Status.objects.all(),
        slug_field='nama_status'
    )

    class Meta:
        model = Produk
        fields = ['nama_produk', 'harga', 'kategori', 'status']

    def validate_nama_produk(self, value):
        if not value.strip():
            raise serializers.ValidationError("Nama produk harus diisi.")
        return value

    def validate_harga(self, value):
        if value <= 0:
            raise serializers.ValidationError("Harga harus lebih besar dari nol.")
        return value

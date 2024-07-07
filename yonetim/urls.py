from django.urls import path

from . import views

urlpatterns = [
    path("", views.yonet, name="yonet"),
    path("kullanicilar/", views.kullanicilar, name="kullanicilar"),
    path("kitaplar/", views.kitaplar, name="kitaplar"),
    path("yazarlar/", views.yazarlar, name="yazarlar"),
    path("yazarlar/guncelle/<int:yazar_id>/", views.yazar_guncelle, name="yazar_guncelle"),
    path("kategoriler/", views.kategoriler, name="kategoriler"),
    path("kategoriler/guncelle/<int:kategori_id>/", views.kategori_guncelle, name="kategori_guncelle"),
    path("yayinevleri/", views.yayinevleri, name="yayinevleri"),
    path("yayinevleri/guncelle/<int:yayinevi_id>/", views.yayinevi_guncelle, name="yayinevi_guncelle"),
    path("yeni-kitap-ekle/", views.yeni_kitap_ekle, name="yeni_kitap_ekle"),
    path("kitaplar/sil/<int:kitap_id>/", views.kitap_sil, name="kitap_sil"),
    path("kitaplar/duzenle/<int:kitap_id>/", views.kitap_duzenle, name="kitap_duzenle"),
    path("giris/", views.giris, name="giris"),
    path("cikis/", views.cikis, name="cikis"),
]
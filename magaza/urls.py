from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("giris/", views.giris, name="giris"),
    path("kayit/", views.kayit, name="kayit"),
    path("cikis/", views.cikis, name="cikis"),
    path("profil/", views.profil, name="profil"),
    path("kitap/<int:id>", views.kitap, name="kitap"),
    path("sepet/ekle/<int:id>", views.ekle, name="ekle"),
    path("sepet/sil/<int:id>", views.sil, name="sil"),
    path("sepet/", views.sepet, name="sepet"),
    path("siparislerim/", views.siparislerim, name="siparislerim"),
    path("odeme/", views.odeme, name="odeme"),
]
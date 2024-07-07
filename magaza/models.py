from django.db import models
from django.contrib.auth.models import User

class Yazar(models.Model):
    ad = models.CharField(max_length=300)

class YayinEvi(models.Model):
    ad = models.CharField(max_length=300)

class Kategori(models.Model):
    ad = models.CharField(max_length=300)

class Kitap(models.Model):
    ad = models.CharField(max_length=300)
    yazar = models.ManyToManyField(Yazar)
    yayin_evi = models.ForeignKey(YayinEvi, on_delete=models.CASCADE)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    basim_yili = models.IntegerField()
    kategori = models.ManyToManyField(Kategori)
    resim = models.TextField()

class Adres(models.Model):
    address = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Siparis(models.Model):
    kitap = models.ManyToManyField(Kitap)
    tamamlandi = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
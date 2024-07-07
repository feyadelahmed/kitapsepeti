import base64
from django.shortcuts import render, redirect
from magaza.models import Kitap, YayinEvi, Yazar, Kategori
from .functions import clear_kat_yzr_yayin, check_input_errors, create_yayinevi, create_kategoriler, create_yazarlar, check_input_errors
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login


def yonet(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")

    context = {}
    return render(request, "yonetim/yonet.html", context)

def cikis(request):
    logout(request)
    return redirect("/yonet/giris")

def giris(request):
    if request.user.is_authenticated:
        if request.user.is_superuser: return redirect("/yonet")
        else: return redirect("/")

    if request.method == "GET":
        return render(request, "yonetim/giris.html")
    
    elif request.method == "POST":
        context = {}
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        context["username"] = username
        context["password"] = password

        if not username or not password:
            context["error"] = "Kullanıcıadı veya Şifre boş olamaz." 
            return render(request, "yonetim/giris.html", context)

        user = authenticate(username=username, password=password)
        if user is None or not user.is_superuser:
            print(user)
            context["error"] = "Kullanıcıadı veya Şifre Yanlıştır." 
            return render(request, "yonetim/giris.html", context)
        else:
            login(request, user)
            return redirect("/yonet")

def kullanicilar(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    users = User.objects.all()
    context = {}
    context["users"] = users
    return render(request, "yonetim/kullanicilar.html", context)

def yazarlar(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    yazarlar = list(Yazar.objects.all())
    context = {"yazarlar": yazarlar}
    return render(request, "yonetim/yazarlar.html", context)

def yazar_guncelle(request, yazar_id):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    yazar = Yazar.objects.get(id=yazar_id)
    yazar.ad = request.POST[f"yazar-{yazar_id}"].strip()
    yazar.save()
    return redirect("/yonet/yazarlar")

def kategoriler(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    kategoriler = list(Kategori.objects.all())
    context = {"kategoriler": kategoriler}
    return render(request, "yonetim/kategoriler.html", context)

def kategori_guncelle(request, kategori_id):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    kategori = Kategori.objects.get(id=kategori_id)
    kategori.ad = request.POST[f"kategori-{kategori_id}"].strip()
    kategori.save()
    return redirect("/yonet/kategoriler")

def yayinevleri(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    yayinevleri = list(YayinEvi.objects.all())
    context = {"yayinevleri": yayinevleri}
    return render(request, "yonetim/yayinevleri.html", context)

def yayinevi_guncelle(request, yayinevi_id):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    yayinevi = YayinEvi.objects.get(id=yayinevi_id)
    yayinevi.ad = request.POST[f"yayinevi-{yayinevi_id}"].strip()
    yayinevi.save()
    return redirect("/yonet/yayinevleri")

def kitaplar(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    kitaplar = []
    db_kitaplar = Kitap.objects.all()
    for k in db_kitaplar:
        kitap = {
            "id": k.id,
            "ad": k.ad,
            "fiyat": k.fiyat,
            "yayin_evi": k.yayin_evi.ad,
            "resim": k.resim,
            "basim_yili": k.basim_yili,
        }

        yazarlar_list = []
        kitap_yazarlar = k.yazar.all()
        for y in kitap_yazarlar:
            yazarlar_list.append(y.ad)

        Kategoriler_list = []
        kitap_kategoriler = k.kategori.all()
        for k in kitap_kategoriler:
            Kategoriler_list.append(k.ad)

        kitap["yazar"] = ", ".join(yazarlar_list)
        kitap["kategori"] = ", ".join(Kategoriler_list)

        kitaplar.append(kitap)

    context = {}
    context["kitaplar"] = kitaplar
    return render(request, "yonetim/kitaplar.html", context)

def kitap_duzenle(request, kitap_id):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    if request.method == "GET":
        k = Kitap.objects.get(id=kitap_id)
        kitap = {
            "id": k.id,
            "ad": k.ad,
            "fiyat": k.fiyat,
            "yayin_evi": k.yayin_evi.ad,
            "resim": k.resim,
            "basim_yili": k.basim_yili,
        }

        yazarlar_list = []
        kitap_yazarlar = k.yazar.all()
        for y in kitap_yazarlar:
            yazarlar_list.append(y.ad)

        Kategoriler_list = []
        kitap_kategoriler = k.kategori.all()
        for k in kitap_kategoriler:
            Kategoriler_list.append(k.ad)

        kitap["yazar"] = ", ".join(yazarlar_list)
        kitap["kategori"] = ", ".join(Kategoriler_list)
        
        context = {"kitap": kitap}
        return render(request, "yonetim/kitap_duzenle.html", context)
    
    elif request.method == "POST":
        errors_check = check_input_errors(request, ignore_resim=True)
        if errors_check["error"]:
            return render(request, "yonetim/kitap_duzenle.html", errors_check["context"])

        ad = request.POST["ad"].strip()
        yazar = request.POST["yazar"].strip()
        kategori = request.POST["kategori"].strip()
        yayin_evi = request.POST["yayin_evi"].strip()
        resim = request.FILES.get("resim")
        basim_yili = int(request.POST["basim_yili"].strip())
        fiyat = float(request.POST["fiyat"].strip())

        yazarlar_list = create_yazarlar(yazar)
        kategoriler_list = create_kategoriler(kategori)
        yayinevi = create_yayinevi(yayin_evi)

        kitap = Kitap.objects.get(id = kitap_id)
        kitap.ad = ad
        kitap.fiyat = fiyat
        kitap.basim_yili = basim_yili    
        kitap.yayin_evi = yayinevi
        if resim:
            base64_resim = f"data:image/*;base64,{base64.b64encode(resim.read()).decode("utf-8")}"
            kitap.resim = base64_resim
        kitap.save()

        kitap.yazar.clear()
        kitap.kategori.clear()

        for y in yazarlar_list:
            kitap.yazar.add(y)

        for k in kategoriler_list:
            kitap.kategori.add(k)

        clear_kat_yzr_yayin()
        
        return redirect(f"/yonet/kitaplar/duzenle/{kitap.id}/")

def kitap_sil(request, kitap_id):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    kitap = Kitap.objects.get(id=kitap_id)
    yayin_evi = kitap.yayin_evi
    yazar = list(kitap.yazar.all())
    kategori = list(kitap.kategori.all())

    print(yazar)

    kitap.delete()
    print(yazar)

    clear_kat_yzr_yayin()

    return redirect("/yonet/kitaplar")

def yeni_kitap_ekle(request):
    if not request.user.is_authenticated:
        return redirect("/yonet/giris")
    elif not request.user.is_superuser:
        return redirect("/")
    
    if request.method != "POST":
        return redirect("/yonet/kitaplar")

    errors_check = check_input_errors(request, ignore_resim=False)
    if errors_check["error"]:
        return render(request, "yonetim/kitaplar.html", errors_check["context"])

    ad = request.POST["ad"].strip()
    yazar = request.POST["yazar"].strip()
    kategori = request.POST["kategori"].strip()
    yayin_evi = request.POST["yayin_evi"].strip()
    resim = request.FILES.get("resim")
    basim_yili = int(request.POST["basim_yili"].strip())
    fiyat = float(request.POST["fiyat"].strip())

    base64_resim = f"data:image/*;base64,{base64.b64encode(resim.read()).decode("utf-8")}"
    yazarlar_list = create_yazarlar(yazar)
    kategoriler_list = create_kategoriler(kategori)
    yayinevi = create_yayinevi(yayin_evi)

    yeni_kitap = Kitap(ad=ad, resim=base64_resim, basim_yili=basim_yili, fiyat=fiyat, yayin_evi=yayinevi)
    yeni_kitap.save()

    for y in yazarlar_list:
        yeni_kitap.yazar.add(y)

    for k in kategoriler_list:
        yeni_kitap.kategori.add(k)

    return redirect("/yonet/kitaplar")

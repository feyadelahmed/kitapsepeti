import base64
from django.shortcuts import render, redirect
from magaza.models import Kitap, Adres, Siparis
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login


def index(request):
    if not request.user.is_authenticated:
        return redirect("/giris")

    context = {}
    tum_kitaplar = list(Kitap.objects.all())
    
    tum_kategoriler = set()
    tum_yazarlar = set()
    tum_yayinevleri = set()
    for k in tum_kitaplar:
        list(map(lambda x: tum_kategoriler.add(x.ad.lower().strip()), k.kategori.all()))
        list(map(lambda x: tum_yazarlar.add(x.ad.lower().strip()), k.yazar.all()))
        tum_yayinevleri.add(k.yayin_evi.ad.lower().strip())
    context["kategoriler"] = list(map(lambda x: {"ad": x, "checked": False}, tum_kategoriler))
    context["yazarlar"] = list(map(lambda x: {"ad": x, "checked": False}, tum_yazarlar))
    context["yayinevleri"] = list(map(lambda x: {"ad": x, "checked": False}, tum_yayinevleri))


    filter_kategoriler = request.GET.getlist("kategoriler")
    filter_yazarlar = request.GET.getlist("yazarlar")
    filter_yayinevleri = request.GET.getlist("yayinevleri")
    kitaplar_filter = tum_kitaplar
    
    if filter_yazarlar:
        filter_yazarlar = list(map(lambda x: x.lower().strip(), filter_yazarlar))
        
        for x in context["yazarlar"]:
            if x["ad"].lower().strip() in filter_yazarlar: x["checked"] = True

        print(context["yazarlar"])
        k_kitaplar = []
        for k in kitaplar_filter:
            k_yazarlar = k.yazar.all()
            for y in k_yazarlar:
                if y.ad.lower().strip() in filter_yazarlar:
                    k_kitaplar.append(k)
                    break
        kitaplar_filter = k_kitaplar

    if filter_kategoriler:
        filter_kategoriler = list(map(lambda x: x.lower().strip(), filter_kategoriler))

        for x in context["kategoriler"]:
            if x["ad"].lower().strip() in filter_kategoriler: x["checked"] = True

        k_kitaplar = []
        for k in kitaplar_filter:
            k_kategoriler = k.kategori.all()
            for y in k_kategoriler:
                if y.ad.lower().strip() in filter_kategoriler:
                    k_kitaplar.append(k)
                    break
        kitaplar_filter = k_kitaplar

    if filter_yayinevleri:
        filter_yayinevleri = list(map(lambda x: x.lower().strip(), filter_yayinevleri))
        for x in context["yayinevleri"]:
            if x["ad"].lower().strip() in filter_yayinevleri: x["checked"] = True

        
        kitaplar_filter = filter(lambda x: x.yayin_evi.ad.lower().strip() in filter_yayinevleri, kitaplar_filter)

    kitaplar = []
    for k in kitaplar_filter:
        kitap = {
            "id": k.id,
            "ad": k.ad,
            "yayin_evi": k.yayin_evi.ad,
            "fiyat": k.fiyat,
            "basim_yili": k.basim_yili,
            "resim": k.resim,
            "yazar": ", ".join(list(map(lambda x: x.ad, k.yazar.all()))),
            "kategori": ", ".join(list(map(lambda x: x.ad, k.kategori.all()))),
        }
        kitaplar.append(kitap)

    user = {
        "ad": request.user.first_name,
        "soyad": request.user.last_name,
    }
    context["user"] = user
    context["kitaplar"] = kitaplar
    return render(request, "magaza/index.html", context)
        
def kitap(request, id):
    if not request.user.is_authenticated:
        return redirect("/giris")

    context = {}
    kitap = Kitap.objects.get(id=id)
    user = {
        "ad": request.user.first_name,
        "soyad": request.user.last_name,
    }
    context["user"] = user
    context["kitap"] = kitap
    return render(request, "magaza/kitap.html", context)
        

def giris(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "GET":
        return render(request, "magaza/giris.html")
    
    elif request.method == "POST":
        context = {}
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        context["username"] = username
        context["password"] = password

        if not username or not password:
            context["error"] = "Kullanıcıadı veya Şifre boş olamaz." 
            return render(request, "magaza/giris.html", context)

        user = authenticate(username=username, password=password)
        if user is None:
            context["error"] = "Kullanıcıadı veya Şifre Yanlıştır." 
            return render(request, "magaza/giris.html", context)
        else:
            login(request, user)
            return redirect("/")
        
def kayit(request):
    if request.user.is_authenticated:
        return redirect("/")

    if request.method == "GET":
        return render(request, "magaza/kayit.html")
    
    elif request.method == "POST":
        context = {}
        firstname = request.POST["firstname"].strip()
        lastname = request.POST["lastname"].strip()
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        context["firstname"] = firstname
        context["lastname"] = lastname
        context["username"] = username
        context["password"] = password

        if not firstname:
            context["error"] = "Ad boş olamaz." 
            return render(request, "magaza/kayit.html", context)

        if not lastname:
            context["error"] = "Soyad boş olamaz." 
            return render(request, "magaza/kayit.html", context)

        if not username:
            context["error"] = "Kullanıcıadı boş olamaz." 
            return render(request, "magaza/kayit.html", context)

        if not password:
            context["error"] = "Şifre boş olamaz." 
            return render(request, "magaza/kayit.html", context)

        users = User.objects.filter(username=username)
        if len(users) > 0:
            context["error"] = "Kullanıcıadı kullanılmış. başka kullanıcıadı seçiniz." 
            return render(request, "magaza/kayit.html", context)
        else:
            user = User.objects.create_user(username=username, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()

            return redirect("/giris")
        
def cikis(request):
    logout(request)
    return redirect("/")

def profil(request):
    if not request.user.is_authenticated:
        return redirect("/giris")
    
    context = {}
    user = {
        "id": request.user.id,
        "ad": request.user.first_name,
        "soyad": request.user.last_name,
        "kullaniciadi": request.user.username,
    }
    try:
        user["adres"] = request.user.adres.address
    except:
        pass
    context["user"] = user

    if request.method != "POST":
        return render(request, "magaza/profil.html", context)

    action = request.GET.get("action")
    if action == "guncelle":
        firstname = request.POST["firstname"].strip()
        lastname = request.POST["lastname"].strip()
        context["firstname"] = firstname
        context["lastname"] = lastname

        if not firstname:
            context["error"] = "Ad boş olamaz." 
            return render(request, "magaza/profil.html", context)

        if not lastname:
            context["error"] = "Soyad boş olamaz." 
            return render(request, "magaza/profil.html", context)
        
        request.user.first_name = firstname
        request.user.last_name = lastname
        request.user.save()
        return redirect("/profil")

    if action == "adres":
        address = request.POST["address"].strip()

        if not address:
            context["adreserror"] = "Adres giriniz." 
            return render(request, "magaza/profil.html", context)
        
        try:
            print("try")
            request.user.adres.address = address
            request.user.adres.save()
            request.user.save()
        except:
            print("try")
            adres = Adres(user=request.user, address=address)
            adres.save()
        return redirect("/profil")

    if action == "sifre":
        oldpassword = request.POST["oldpassword"].strip()
        newpassword = request.POST["newpassword"].strip()

        if not oldpassword or not newpassword:
            context["sifreerror"] = "Yeni ve Eski Şifreyi giriniz." 
            return render(request, "magaza/profil.html", context)

        u = authenticate(username=request.user.username, password=oldpassword)
        if u is None:
            context["sifreerror"] = "Eski Şifre yanlıştır." 
            return render(request, "magaza/profil.html", context)
        request.user.set_password(newpassword)
        request.user.save()
        return redirect("/cikis")
    
    if action == "sil":
        password = request.POST["password"].strip()
        if not password:
            context["silerror"] = "Şifreyi giriniz." 
            return render(request, "magaza/profil.html", context)

        u = authenticate(username=request.user.username, password=password)
        if u is None:
            context["silerror"] = "Şifre yanlıştır." 
            return render(request, "magaza/profil.html", context)
        request.user.delete()
        return redirect("/cikis")
    return redirect("/profil")

def ekle(request, id):
    if not request.user.is_authenticated:
        return redirect("/giris")
    sepet = Siparis.objects.filter(user=request.user, tamamlandi=False)
    if len(sepet) > 0:
        sepet[0].kitap.add(Kitap.objects.get(id=id))
    else:
        print("not found")
        sepet = Siparis.objects.create(user=request.user, tamamlandi=False)
        sepet.kitap.add(Kitap.objects.get(id=id))

    return redirect("/sepet")

def sil(request, id):
    if not request.user.is_authenticated:
        return redirect("/giris")

    sepet = Siparis.objects.get(user=request.user, tamamlandi=False)
    sepet.kitap.remove(Kitap.objects.get(id=id))
    return redirect("/sepet")

def odeme(request):
    if not request.user.is_authenticated:
        return redirect("/giris")

    sepet = Siparis.objects.get(user=request.user, tamamlandi=False)
    sepet.tamamlandi = True
    sepet.save()
    return redirect("/sepet")

def sepet(request):
    if not request.user.is_authenticated:
        return redirect("/giris")
    
    sepet = Siparis.objects.filter(user=request.user, tamamlandi=False)
    if len(sepet) == 0:
        return render(request, "magaza/sepet.html")
    else:
        sepet_kitaplar = sepet[0].kitap.all()
        print(sepet[0].user.id)
        kitaplar = []

        for k in sepet_kitaplar:
            kitap = {
                "id": k.id,
                "ad": k.ad,
                "yayin_evi": k.yayin_evi.ad,
                "fiyat": k.fiyat,
                "basim_yili": k.basim_yili,
                "resim": k.resim,
                "yazar": ", ".join(list(map(lambda x: x.ad, k.yazar.all()))),
                "kategori": ", ".join(list(map(lambda x: x.ad, k.kategori.all()))),
            }
            kitaplar.append(kitap)
        
        context = {}
        context["kitaplar"] = kitaplar
        return render(request, "magaza/sepet.html", context)

def siparislerim(request):
    if not request.user.is_authenticated:
        return redirect("/giris")
    
    sepet = Siparis.objects.filter(user=request.user, tamamlandi=True)
    if len(sepet) == 0:
        return render(request, "magaza/siparislerim.html")
    else:
        siparisler = []
        for k in list(sepet):
            kitaplar = k.kitap.all()
            s_kitaplar = []

            for k in kitaplar:
                kitap = {
                    "id": k.id,
                    "ad": k.ad,
                    "yayin_evi": k.yayin_evi.ad,
                    "fiyat": k.fiyat,
                    "basim_yili": k.basim_yili,
                    "resim": k.resim,
                    "yazar": ", ".join(list(map(lambda x: x.ad, k.yazar.all()))),
                    "kategori": ", ".join(list(map(lambda x: x.ad, k.kategori.all()))),
                }
                s_kitaplar.append(kitap)
            siparisler.append(s_kitaplar)

        context = {}
        context["siparisler"] = siparisler
        return render(request, "magaza/siparislerim.html", context)

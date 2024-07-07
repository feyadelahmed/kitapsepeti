from magaza.models import Kitap, YayinEvi, Yazar, Kategori

def is_valid_price(fiyat):
    fiyat = fiyat.strip()
    if not fiyat: return False
    else:
        try:
            fiyat_float = float(fiyat)
            if fiyat_float < 0: return False
        except:
            return False
    return True

def is_valid_year(basim_yili):
    basim_yili = basim_yili.strip()
    if not basim_yili or len(basim_yili) != 4 or not basim_yili.isdigit() or int(basim_yili) < 0:
        return False
    return True

def is_empty(string):
    return not string

def check_input_errors(request, ignore_resim):
    context = {}
    error_list = {}

    ad = request.POST["ad"]
    if is_empty(ad): error_list["ad"] = "kitap adı boş olamaz."

    yazar = request.POST["yazar"]
    if is_empty(yazar): error_list["yazar"] = "en az bir yazar adı girmelisiniz."

    kategori = request.POST["kategori"]
    if is_empty(kategori): error_list["kategori"] = "en az bir kategori girmelisiniz."

    yayin_evi = request.POST["yayin_evi"]
    if is_empty(yayin_evi): error_list["yayin_evi"] = "yayınevi adı boş olamaz."

    if not ignore_resim:
        resim = request.FILES.get("resim")
        if is_empty(resim): error_list["resim"] = "kitap resmi boş olamaz."

    basim_yili = request.POST["basim_yili"]
    if not is_valid_year(basim_yili): error_list["basim_yili"] = "basım yılı bir yıl olmalı (ör. 2004)."

    fiyat = request.POST["fiyat"]
    if not is_valid_price(fiyat): error_list["fiyat"] = "fiyat sıfırdan büyük bir tamsayı olmalı."

    if len(error_list) > 0:
        context["errors"] = error_list
        context["values"] = {
            "ad": ad,
            "basim_yili": basim_yili,
            "fiyat": fiyat,
            "yayin_evi": yayin_evi,
            "yazar": yazar,
            "kategori": kategori,
        }
        
        return {"error": True, "context": context}
    else:
        return {"error": False}

def create_yazarlar(yazar_str):
    yazarlar_list = []
    yazarlar = yazar_str.split(",")
    for y in yazarlar:
        y = y.strip()
        if not y: continue
        db_yazar = Yazar.objects.filter(ad=y)
        if len(db_yazar) > 0:
            yazarlar_list.append(db_yazar[0])
            continue
        yeni_yazar = Yazar(ad=y)
        yeni_yazar.save()
        yazarlar_list.append(yeni_yazar)
    return yazarlar_list

def create_kategoriler(kategori_str):
    kategoriler_list = []
    kategoriler = kategori_str.split(",")
    for k in kategoriler:
        k = k.strip()
        if not k: continue
        db_kategori = Kategori.objects.filter(ad=k)
        if len(db_kategori) > 0:
            kategoriler_list.append(db_kategori[0])
            continue
        yeni_kategori = Kategori(ad=k)
        yeni_kategori.save()
        kategoriler_list.append(yeni_kategori)
    return kategoriler_list

def create_yayinevi(yayinevi_str):
    db_yayinevi = YayinEvi.objects.filter(ad=yayinevi_str)
    if len(db_yayinevi) == 0:
        yeni_yayinevi = YayinEvi(ad=yayinevi_str)
        yeni_yayinevi.save()
    return YayinEvi.objects.get(ad=yayinevi_str)

def clear_kat_yzr_yayin():
    yazarlar = Yazar.objects.all()
    kategoriler = Kategori.objects.all()
    yayinevleri = YayinEvi.objects.all()
    
    for y in yazarlar:
        if len(y.kitap_set.all()) == 0:
            y.delete()
    
    for k in kategoriler:
        if len(k.kitap_set.all()) == 0:
            k.delete()
    
    for ye in yayinevleri:
        if len(ye.kitap_set.all()) == 0:
            ye.delete()
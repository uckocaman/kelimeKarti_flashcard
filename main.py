# -*- coding:utf-8 -*-
import random
import json

def kelimeEkle(x):
    """
    Kullanıcı kelime dosyası varsa ona kelime ekler. Dosyası yoksa da daha sonra dosya olarak kaydetmek üzere uygulama içinde sözlük olarak yeni kelime eklemesini sağlar.
    x yani fonksiyonun girdisi kelimelerin ekleneceği varsa dosya -json olduğu için o da sözlük- yoksa boş sözlüktür.  
    """
    while True:
        print("Kelime ekleme işlemini bitirmek için 'q', listenin güncel halini görmek için 'L' tuşuna basabilirsiniz.")
        kelime = str(input("Kelimenizi giriniz: ")).lower().strip()
        if kelime == 'q':
            break
        elif kelime == 'l':
            print(f"Kelimeleriniz : {x}") #listenin güncel hali
            continue
        elif len(kelime) == 0:
            print("Boş karakter giremezsiniz.")
            continue
        else:
            anlami= str(input("Anlamını  giriniz: ")).strip()
            x[kelime] = anlami # kelime ve anlamının sözlüğe eklenmesi
            print(f"{kelime} eklendi.")
    print(f"Kelimeleriniz : {x}")
    return x

def kelimeSilme(x):
    """
    Kullanıcının dışarıdan yüklediği kelime dosyasından veya uygulama içinde oluşturduğu dosyadan istediği kelimeleri silmesini sağlar.
    x yani fonksiyonun girdisi kelimelerin silineceği varsa dosya -json olduğu için o da sözlük- yoksa boş sözlüktür.
    """
    while True:
        if len(x) == 0:
            print("Listenizde hiç kelime yok. Bu yüzden silme işlemi yapamazsınız.")
            break
        else:
            silinecekKelime = str(input("Silmek istediğiniz kelimeyi giriniz. Çıkmak için 'q' tuşuna basınız\n")).strip().lower()
            if silinecekKelime == 'q':
                break
            else:
                try:
                    x.pop(silinecekKelime) # kelimenin sislinmesi
                    print(f"{silinecekKelime} silindi.")
                except KeyError:
                    print("Bu kelime zaten yok. Doğru girdiğinizden emin olun.")
    print(f"Kelime listenizin son durumu: {x}")
    return x

def oyun(x):
    """
    Kullanıcının kelimelerin anlamlarını tahmin ettiği ve bu tahminlerin kaç tanesinin doğru veya yanlış olduğunun hesaplandığı uygulamanın ana bölümdür. 
    Kullanıcıya iki seçenek sunulur. İsterse uygulama ona bir kelimeyi sorar ve kullanıcı anlamını tahmin eder, isterse de uygualama ona  kelimenin anlamını verir 
    kullanıcı da onun hangi kelimeye karşılık geldiğini tahmin etmesini ister.
    """
    gecici_dict = {}
    gecici_dict.update(x) # sorulan bir kelimenin bir daha sorulmaması için sorulan kelimeler siliniyor. Bu işlem de verileri kaybetmemek için geçici bir değişken üzerinden yapılıyor.
    # x'i direkt gecici_dict'e tanımlasaydık sözlükler referans türünde olduğu için x ile aynı adresi taşıyacaktı ve yapılan değişiklik her ikisini de etkileyecekti. update ile bu engellenmiş oldu.
    yanlis_sayisi=0 
    dogru_sayisi=0
    soru_sayisi=0
    while True:
        try:
            abc = int(input("**********\n1- Kelimeden anlamını tahmin et\n2- Anlamından kelimeyi tahmin et\n"))
            if abc == 1:
                for i in range(len(x)):
                    key, val = random.choice(list(gecici_dict.items())) # kelime dosyasından rastgele bir kelime seçilip kelime key değişkenine, anlamı val değişkenine atanıyor.
                    tahmin = str(input(f"'{key}' kelimesinin anlamı nedir? Doğru cevabı görmek için 'c' ye, cikmak icin 'q'ya basin.\n")).strip().lower()
                    if tahmin == 'c':
                        print(f"'{key}' kelimesinin anlamı '{val}'")
                    elif tahmin == 'q':
                        break #çıkış
                    else:
                        if str(tahmin) == val: 
                            print("Doğru bildiniz")
                            dogru_sayisi +=1
                        else:
                            yanlis_sayisi +=1
                            print(f"Yanlış bildiniz. Doğru cevap '{val}'")
                        gecici_dict.pop(key) # sorulan kelimenin tekrar sorulmaması için silinmesi
                    soru_sayisi +=1
                print(f"{soru_sayisi} soruda {dogru_sayisi} dogru, {yanlis_sayisi} yanlis yaptınız.")
                break

            elif abc == 2:
                for i in range(len(x)):
                    key, val = random.choice(list(gecici_dict.items()))
                    tahmin = input(f"'{val}' hangi kelimeye karşılık gelmektedir? Doğru cevabı görmek için 'c' ye, cikmak icin 'q'ya basin.\n").lower().strip() 
                    if tahmin == 'c':
                        print(f"'{val}', '{key}' kelimesine karşılık gelmektedir.")
                    elif tahmin == 'q':
                        break
                    else:
                        if str(tahmin) == key:
                            print("Doğru bildiniz")
                            dogru_sayisi +=1
                        else:
                            yanlis_sayisi +=1
                            print(f"Yanlış bildiniz. Doğru cevap {key}")
                        gecici_dict.pop(key)
                    soru_sayisi += 1
                print(f"{soru_sayisi} soruda {dogru_sayisi} dogru, {yanlis_sayisi} yanlis yaptınız.")
                break
            else:
                print("Hatalı Giriş yaptınız. 1'i veya 2'yi seçin.") # 1 veya 2 dışındaki bir sayı girilirse
        except ValueError:
            print("Hatalı giriş yaptınız. 1'i veya 2'yi seçin.") # sayı dışında bir değer girilirse

def dosyaKaydet(x):
    """
    Dosyası olmayan kullanıcının eklediği kelimelerin tekrar kullanılabilmesi için .json olarak kayıt edilmesi.
    """
    while True:
        try:
            dosyaAdi = str(input("Dosyaya vermek istediğiniz ismi .json uzantısı ile birlikte giriniz. 'kelime.json' gibi\n"))
            with open(dosyaAdi, "w", encoding="utf-8") as dosya:
                json.dump(x, dosya)
                break
        except FileNotFoundError:
            print("Dosya ismi boşluk olamaz. Lütfen kullanılabilir bir isim giriniz.")

def dosyaGuncelle(x,y):
    """
    Dosya ile çalışan kullanıcının ekleme veya çıkarma yapması durumunda dosyasının güncellenmesi. x dosya adını ye ise kelimelerin olduğu sözlüğü ifade ediyor.
    """
    with open(y, "w", encoding="utf-8") as dosya:
        json.dump(x, dosya)

while True:
    try:
        dosyaVarMi = int(input(".json uzantılı kelime dosyanız var mı?\n1- Var\n2- Yok\n3- Çıkış\n"))
        if dosyaVarMi == 1:
            dosyaAdi = str(input("Dosya adınınızı .json uzantısı ile birlikte girin ve bu program ile aynı dizinde olduğundan emin olun. Üst menüye dönmek için 'q'ya basabilirsiniz.\n"))
            while True:
                try:
                    if dosyaAdi.lower() == 'q':
                        break
                    else:
                        with open(dosyaAdi, encoding= "utf-8") as dosya: #kullanıcının dosyasının açılması
                            dosyaKelimeler = json.load(dosya) # dosya içeriğinin dosyaKelimeler değişkenine atanması
                        try:
                            islem = int(input("Yapmak istediginiz islemi seciniz: \n1- Oyuna başla \n2- Kelime Ekleme \n3- Kelime Silme \n4- Üst Menü\n"))
                            if islem == 1:
                                oyun(dosyaKelimeler)
                            elif islem == 2:
                                kelimeEkle(dosyaKelimeler)
                                dosyaGuncelle(dosyaKelimeler,dosyaAdi) # keime ekleme işlemi bittikten sonra otomatik olarak dosya güncelleniyor.
                            elif islem == 3:
                                kelimeSilme(dosyaKelimeler)
                                dosyaGuncelle(dosyaKelimeler,dosyaAdi) # keime silme işlemi bittikten sonra otomatik olarak dosya güncelleniyor.
                            elif islem == 4:
                                break
                            else:
                                print("Hatalı giris yaptınız. 1-4 arası bir değer giriniz.")
                        except ValueError:
                            print("Hatalı giris yaptınız. 1-4 arası bir değer giriniz.")
                except FileNotFoundError:
                    print("Dosya Bulunamadı.") # girilen isimde bir dosyanın bulunmaması
                    break
                
        elif dosyaVarMi == 2:
            # kullanıcının kelime dosyası olmadığındna uygulamanın çalışabilmesi için öncelikle kelime eklemesi gerekmektedir. Bu yüzden kelimeEkle() fonksiyonu ilk olarak çalıştırılır.
            print("Kelime dosyanız olmadığı için ilk önce öğrenmek istediğiniz kelimeleri eklemelisiniz.")
            kelimeler = {}
            kelimeEkle(kelimeler)
            while True:
                try:
                    islem = int(input("Yapmak istediginiz islemi seciniz:\n1- Oyuna başla\n2- Kelime Ekleme\n3- Kelime Silme\n4- Kelimeleri .json olarak kaydet\n5- Üst Menü\n"))
                    if islem == 1:
                        oyun(kelimeler)
                    elif islem == 2:
                        kelimeEkle(kelimeler)
                    elif islem == 3:
                        kelimeSilme(kelimeler)
                    elif islem == 4:
                        dosyaKaydet(kelimeler)
                    elif islem == 5:
                        break
                    else:
                        print("Hatalı giris yaptınız. 1-5 arası bir değer giriniz.")
                except ValueError:
                    print("Yanlış değer girdiniz. 1-5 arası bir değer girin.")
        elif dosyaVarMi == 3:
            break
        else:
            print("Yanlış değer girdiniz.\n") #1-2-3 dışında değer girilmesi
    except ValueError:
        print("Yanlış değer girdiniz.\n") # int dışında değer girilmesi
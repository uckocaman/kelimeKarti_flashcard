import sys
import json
import random
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMainWindow, QApplication, QButtonGroup
from PyQt5.QtGui import QIcon
from main_tasarım_code import Ui_MainWindow

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dogru = 0
        self.yanlis = 0
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(550,130,880,840)
        self.ui.btnGozat.clicked.connect(self.onClickedGozat)
        self.ui.btnSor.clicked.connect(self.onClickedYonlendirme)
        self.ui.btnKontrol.clicked.connect(lambda : self.onClickedKontrol(key,val))
        self.ui.btnBitir.clicked.connect(self.onClickedBitir)
        self.ui.btnEkle.clicked.connect(lambda : self.kelimeEkle(dosya))
        self.ui.btnSil.clicked.connect(lambda : self.kelimeSil(dosya))
        self.ui.btnKaydet.clicked.connect(lambda : self.dosyaKaydet(dosya))
        self.ui.btnDosyaOlustur.clicked.connect(self.dosyaOlustur)
        self.ui.btnDosyaOlustur.clicked.connect(self.dosyaOlustur)
        self.ui.rbKelimedenTanim.pressed.connect(self.onClickedSor)
        self.ui.rbTanimdanKelime.pressed.connect(self.onClickedSor2)

        self.group = QButtonGroup()
        self.group.addButton(self.ui.rbKelimedenTanim)
        self.group.addButton(self.ui.rbTanimdanKelime) 
        

        try:
            self.ui.kelimeInput.returnPressed.connect(lambda : self.onClickedKontrol(key,val))
            self.ui.etEklenecekAnlam.returnPressed.connect(lambda : self.kelimeEkle(dosya))
            self.ui.etSilinecekKelime.returnPressed.connect(lambda : self.kelimeSil(dosya))
            self.ui.etdosyaAdi.returnPressed.connect(lambda : self.dosyaKaydet(dosya))
        except KeyError:
            pass

    def dosyaOlustur(self):
        global dosya
        dosya = {}
        global dosyaIlk
        dosyaIlk = {}
        self.ui.lblDosyaOlusturuldu.setText("Dosyanız oluşturuldu. Oyuna başlayabilmek için önce aşağıdan kelime eklemelisiniz. Daha sonra isterseniz dosyanızı kayıt edebilirsiniz.")
        self.ui.btnEkle.setEnabled(True)
        if len(dosya) > 0:
            self.ui.btnKaydet.setEnabled(True)
            self.ui.btnSor.setEnabled(True)
        return dosya

    def dosyaKaydet(self, dosya):
        dosyaAdi = self.ui.etdosyaAdi.text()
        try:
            with open(dosyaAdi, "w", encoding="utf-8") as d:
                json.dump(dosya, d)
                self.ui.lblDosyaEklendi.setText(f"{dosyaAdi} dosyası kayıt edildi.")
        except FileNotFoundError:
            self.ui.lblDosyaEklendi.setText("Dosya ismi boşluk olamaz. Lütfen kullanılabilir bir isim giriniz.")
        return dosya

    def kelimeSil(self, dosya):
        silinecekKelime = self.ui.etSilinecekKelime.text()
        try: 
            dosya.pop(silinecekKelime) 
            self.ui.lblKelimeSilindi.setText(f"{silinecekKelime} silindi.")
            self.ui.etSilinecekKelime.setText("")
            self.ui.btnKaydet.setEnabled(True)
        except KeyError:
            self.ui.lblKelimeSilindi.setText(f"Dosyanızda {silinecekKelime} kelimesi zaten yok.")
            self.ui.etSilinecekKelime.setText("")
        if len(dosya) == 0:
            self.ui.btnKaydet.setEnabled(False)
            self.ui.btnSor.setEnabled(False)
            self.ui.btnKontrol.setEnabled(False)
            self.ui.btnBitir.setEnabled(False)
            self.ui.btnSil.setEnabled(False)
            self.ui.rbKelimedenTanim.setEnabled(False)
            self.ui.rbTanimdanKelime.setEnabled(False)
        return dosya

    def kelimeEkle(self,dosya):
        eklenecekKelime = self.ui.etEklenecekKelime.text()
        eklenecekAnlam = self.ui.etEklenecekAnlam.text()
        if len(eklenecekKelime) == 0 or len(eklenecekAnlam) == 0:
            self.ui.lblKelimeEklendi.setText("Bosluk ekleyemezsiniz. Lütfen bir kelime ve anlamını girin.")
        else:
            dosya[eklenecekKelime] = eklenecekAnlam
            self.ui.lblKelimeEklendi.setText(f"{eklenecekKelime} eklendi.")
            self.ui.etEklenecekKelime.setText("")
            self.ui.etEklenecekAnlam.setText("")
            self.ui.btnSor.setEnabled(True)
            dosyaIlk.update(dosya)
        if len(dosya) > 0:
            self.ui.btnSil.setEnabled(True)
            self.ui.btnKaydet.setEnabled(True)
            self.ui.rbKelimedenTanim.setEnabled(True)
            self.ui.rbTanimdanKelime.setEnabled(True)
        return dosya
    
    def onClickedBitir(self):
        self.ui.lblSonuc.setText(f"{self.dogru} dogru, {self.yanlis} yanlis")
        self.ui.btnKontrol.setEnabled(False)
        self.ui.rbTanimdanKelime.setEnabled(True)
        self.ui.rbKelimedenTanim.setEnabled(True)

    def onClickedGozat(self):
        filen = QFileDialog.getOpenFileName()
        path = filen[0]
        dosyaAdi2 = path.split("/")
        global dosya
        global dosyaIlk
        dosyaIlk = {}
        with open(path, encoding= "utf-8") as d:
            dosya = json.load(d)
            self.ui.lblGozatOkundu.setText(f"{dosyaAdi2[-1]} okundu.")
            self.ui.etdosyaAdi.setText(dosyaAdi2[-1])
        dosyaIlk.update(dosya)
        if len(dosya) > 0:
            self.ui.btnSil.setEnabled(True)
        self.ui.btnSor.setEnabled(True)
        self.ui.btnEkle.setEnabled(True)
        self.ui.rbKelimedenTanim.setEnabled(True)
        self.ui.rbTanimdanKelime.setEnabled(True)
        self.ui.btnGozat.setEnabled(False)
        self.ui.btnDosyaOlustur.setEnabled(False)

    def onClickedYonlendirme(self):
        if self.ui.rbKelimedenTanim.isChecked():
            self.group.setExclusive(True)        
            self.ui.btnSor.clicked.connect(self.onClickedSor)
        elif self.ui.rbTanimdanKelime.isChecked():
            self.group.setExclusive(True)        
            self.ui.btnSor.clicked.connect(self.onClickedSor2)
        # self.group.setExclusive(False)             

    def onClickedSor(self):
        self.ui.kelimeInput.clear()
        global key,val
        key, val = random.choice(list(dosyaIlk.items()))
        self.ui.lblCevap.setText(" ")
        self.ui.lblSorulanKelime.setText(key)
        self.ui.btnKontrol.setEnabled(True)
        self.ui.btnBitir.setEnabled(True)
        self.ui.rbTanimdanKelime.setEnabled(False)
        return key, val
        
    def onClickedSor2(self):
        self.ui.kelimeInput.clear()
        global key,val
        key, val = random.choice(list(dosyaIlk.items()))
        self.ui.lblCevap.setText(" ")
        self.ui.lblSorulanKelime.setText(val)
        self.ui.btnKontrol.setEnabled(True)
        self.ui.btnBitir.setEnabled(True)
        self.ui.rbKelimedenTanim.setEnabled(False)
        return key, val

    def onClickedKontrol(self,key,val):
        cevap = self.ui.kelimeInput.text()
        self.ui.btnKontrol.setEnabled(False)
        
        if self.ui.rbKelimedenTanim.isChecked():
            if cevap == val:
                self.ui.lblCevap.setText("Doğru")
                self.dogru += 1
                try:
                    dosyaIlk.pop(key)
                except KeyError:
                    pass
            else:
                self.ui.lblCevap.setText(f"Yanlış. Cevap {val}.")
                self.yanlis += 1
        elif self.ui.rbTanimdanKelime.isChecked():
            if cevap == key:
                self.ui.lblCevap.setText("Doğru")
                self.dogru += 1
                try:
                    dosyaIlk.pop(key)
                except KeyError:
                    pass
            else:
                self.ui.lblCevap.setText(f"Yanlış. Cevap {key}.")
                self.yanlis += 1

        if len(dosya) == 0:
            self.ui.btnSor.setEnabled(False)
            self.ui.btnKontrol.setEnabled(False)
            self.ui.lblSonuc.setText("Tüm kelimeleri kullandınız")

def flashCard():
    app = QApplication(sys.argv)
    win = main()
    win.show()
    sys.exit(app.exec_())
flashCard()
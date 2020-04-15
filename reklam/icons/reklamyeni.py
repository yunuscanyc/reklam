# encoding:utf-8
import time,os,sys,getpass
from PySide2 import QtCore, QtWidgets,  QtGui,QtUiTools
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *
from ftplib import FTP
from pathlib import Path
import video,ast
from time import sleep
from datetime import datetime
from urllib.request import urlopen
import mysql.connector
import socket
import gmplot
import subprocess
import asyncio
from pythonping import ping
from PySide2.QtWebEngineWidgets import *
from PySide2.QtMultimedia import QMediaContent, QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget
class Giris(QtWidgets.QMainWindow):
    def baslat(self):

        kontroledilecek=[]
        for i in range(self.window.cihazlar.rowCount()):
            kontroledilecek.append([self.window.cihazlar.item(i,3).text(),i])
        asyncio.run(self.kontrolet(kontroledilecek))

    def internet_on(self):
        try:
            response = urlopen('https://www.google.com/', timeout=10)
            return True
        except:
            return False
    def __init__(self, parent=None):
        super(Giris, self).__init__(parent)
        self.clicked=False
        self.mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)






        loader = QtUiTools.QUiLoader()
        file = QtCore.QFile(os.path.abspath("ui/reklam.ui"))
        file.open(QtCore.QFile.ReadOnly)
        self.window = loader.load(file, parent)
        file.close()
        self.window.move(200,20)
        self.saatler=dict()
        for i in range(0,24):
            if (len(str(i))==1):
                j="0"+str(i)
            else:
                j=str(i)
            self.saatler[j+":00-"+j+":59"]=[]
        self.ayarlar=dict()
        try:
            mySql_select_query = """select * from ayarlar"""
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query)
            myresult = cursor.fetchall()
            cursor.close()
            self.ayarlar["ftp"]=[myresult[0][2],myresult[0][3],myresult[0][4],myresult[0][5]]
            self.ayarlar["stil"]=myresult[0][9]
            self.ayarlar["arkaplan"]=[myresult[0][7],myresult[0][8]]
        except:
            print("ayarlar yüklenemedi.")
        finally:
            self.mydb.disconnect()
        self.style_string=""
        try:
            with open("./icons/" + self.ayarlar["stil"] + ".qss","r") as file:
                data = file.read()
            for dat in data:
                self.style_string=self.style_string + dat
        except:
            pass
        self.window.setStyleSheet(self.style_string)
        self.acAct = QAction(QIcon('./icons/open.png'), "Görevleri Aç", self)
        self.acAct.triggered.connect(self.ac)
        self.acAct.setShortcut('Ctrl+O')
        self.idekleAct = QAction(QIcon('./icons/addid.png'), "Cihaz Ekle", self)
        self.idekleAct.triggered.connect(self.cihaz_ekleGoster)
        self.taskekleAct = QAction(QIcon('./icons/addtask.png'), "Görev Ekle", self)
        self.taskekleAct.triggered.connect(lambda:self.gorev_ekleGoster(""))
        self.grupekleAct = QAction(QIcon('./icons/addgrup.png'), "Grup Ekle", self)
        self.grupekleAct.triggered.connect(self.grup_ekleGoster)
        self.kaydetAct = QAction(QIcon('./icons/save.png'), "Görevleri Kaydet", self)
        self.kaydetAct.triggered.connect(self.kaydetGorev)
        self.cikisAct = QAction(QIcon('./icons/quit.png'), "Çıkış", self)
        self.cikisAct.triggered.connect(self.cikis)
        self.ayarlarAct = QAction(QIcon('./icons/settings.png'), "Ayarlar", self)
        self.ayarlarAct.triggered.connect(self.ayar)
        self.mapAct = QAction(QIcon('./icons/map.png'), "Cihaz Bilgisi", self)
        self.mapAct.triggered.connect(self.cihazGoster)
        self.uploadAct = QAction(QIcon('./icons/upload.png'), "Kaydet ve Yayınla", self)
        self.uploadAct.triggered.connect(self.uploadDef)
        self.window.tool.setIconSize(QSize(60,60))
        self.window.tool.addAction(self.acAct)
        self.window.tool.addAction(self.idekleAct)
        self.window.tool.addAction(self.taskekleAct)
        self.window.tool.addAction(self.grupekleAct)
        self.window.tool.addAction(self.kaydetAct)
        self.window.tool.addAction(self.ayarlarAct)
        self.window.tool.addAction(self.mapAct)
        self.window.tool.addAction(self.cikisAct)
        Spacer = QWidget()
        Spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.controlLayout = QHBoxLayout()
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.positionSlider)

        self.videoWidget=QVideoWidget()

        self.window.layout1.addWidget(self.videoWidget)
        self.window.layout1.addLayout(self.controlLayout)
        self.window.layout1.addWidget(self.errorLabel)

        self.fileName=""

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)






        self.window.tool.addWidget(Spacer)
        self.window.tool.addAction(self.uploadAct)
        self.window.tool.setMovable(False)
        self.window.tablo.setHorizontalHeaderLabels(["DOSYA","ID'LER","ZAMANLAR","İŞLEM"])
        header = self.window.tablo.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        self.window.tablo.setColumnWidth(0, 200)
        self.window.tablo.setColumnWidth(1, 250)
        self.window.tool.setContextMenuPolicy(Qt.PreventContextMenu)

        self.window.tablo.setShowGrid(True)
        self.window.tablo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.window.tablo.setEditTriggers(QAbstractItemView.NoEditTriggers)


        self.window.tablo.setStyleSheet("QTableWidget::item { padding: 0px }")
        self.progressBar = QProgressBar()
        self.window.statusBar().showMessage('Hazır')

        self.window.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar2 = QProgressBar()
        self.window.statusBar().addPermanentWidget(self.progressBar2)

        self.progressBar.setGeometry(20, 40, 100, 25)
        self.progressBar.setValue(0)
        self.progressBar2.setGeometry(20, 40, 100, 25)
        self.progressBar2.setValue(0)
        self.progressBar.setVisible(False)
        self.progressBar2.setVisible(False)
        self.window.radioKay.toggled.connect(self.toggleRadio)
        self.window.radioYay.toggled.connect(self.toggleRadio)
        self.window.radioKay.setChecked(Qt.Checked)
        self.window.gorevler.doubleClicked.connect(self.tamamGorev)

        self.mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )

        self.gruplarial()


        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.window.sec.sizePolicy().hasHeightForWidth())
        self.window.sec.setSizePolicy(sizePolicy2)
        self.window.sec.setMinimumSize(QSize(50, 0))

        self.window.hepsini.stateChanged.connect(self.secim)
        self.window.sec.clicked.connect(self.dosyaSec)
        self.window.tamam.clicked.connect(self.ekleme)
        self.window.iptal.clicked.connect(lambda: self.window.stacked.setCurrentIndex(0))


        for i in range(0,24):
            if (len(str(i))==1):
                j="0"+str(i)
            else:
                j=str(i)
            item = QListWidgetItem()
            item.setText("{}".format(j+":00-"+j+":59"))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.window.listWidget.addItem(item)
        self.window.cmbid.addItem("Hepsini Seç")
        self.window.cmbid.addItem("Hepsini Kaldır")
        for key in self.gruplar:
            self.window.cmbid.addItem(key)

        self.window.cmbid.currentTextChanged.connect(self.combo_sec)
        self.window.iptal.setText(QtWidgets.QApplication.translate("Dialog", "İPTAL", None, -1))
        self.window.tamam.setIcon(QIcon("./icons/ok.png"))
        self.window.iptal.setIcon(QIcon("./icons/cancel.png"))
        self.window.iptal.setIconSize(QSize(20, 20))
        self.window.tamam.setIconSize(QSize(20, 20))
        self.window.sec.setIcon(QIcon("./icons/choose.png"))
        self.window.sec.setIconSize(QSize(20, 20))

        self.window.idlist.connect(self.window.idlist,QtCore.SIGNAL("customContextMenuRequested(QPoint)" ), self.listItemRightClickedCihaz)

        self.window.tamamCihaz.clicked.connect(lambda: self.window.stacked.setCurrentIndex(0))
        self.window.idlist.itemClicked.connect(self.tiklandiCihaz)
        self.window.ekleCihaz.clicked.connect(self.eklemeCihaz)
        self.mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )
        self.doldurCihaz()
        self.window.tamamCihaz.setText(QtWidgets.QApplication.translate("Dialog", "DÖN", None, -1))
        self.window.ekleCihaz.setText(QtWidgets.QApplication.translate("Dialog", "EKLE", None, -1))
        self.window.tamamCihaz.setIcon(QIcon("./icons/cancel.png"))
        self.window.tamamCihaz.setIconSize(QSize(20, 20))
        self.window.ekleCihaz.setIcon(QIcon("./icons/add.png"))
        self.window.ekleCihaz.setIconSize(QSize(20, 20))

        self.window.tamamGrup.clicked.connect(self.tamamdirGrup)
        self.window.iptalGrup.clicked.connect(lambda: self.window.stacked.setCurrentIndex(0))
        self.window.silGrup.clicked.connect(self.silDefGrup)
        self.window.combo.activated.connect(self.combo_secGrup)
        self.window.combo.addItem("Seçiniz veya Yeni İsim Giriniz")

        self.window.tamamGrup.setIcon(QIcon("./icons/ok.png"))
        self.window.iptalGrup.setIcon(QIcon("./icons/cancel.png"))
        self.window.iptalGrup.setIconSize(QSize(20, 20))
        self.window.tamamGrup.setIconSize(QSize(20, 20))
        self.window.silGrup.setIcon(QIcon("./icons/delete.png"))
        self.window.silGrup.setIconSize(QSize(20, 20))
        self.window.tamamGrup.setText(QtWidgets.QApplication.translate("Dialog", "KAYDET", None, -1))
        self.window.iptalGrup.setText(QtWidgets.QApplication.translate("Dialog", "ÇIKIŞ", None, -1))
        self.window.silGrup.setText(QtWidgets.QApplication.translate("Dialog", "SİL", None, -1))
        self.window.sabit.clicked.connect(self.yuklesabit)
        self.window.arkaplan.clicked.connect(self.yuklearkaplan)
        icon1 = QIcon()
        icon1.addFile(u"../icons/ok.png", QSize(), QIcon.Normal, QIcon.Off)
        self.window.tamamAyar.setIcon(icon1)
        self.window.tamamAyar.setIconSize(QSize(20, 20))
        icon = QIcon()
        icon.addFile(u"../icons/cancel.png", QSize(), QIcon.Normal, QIcon.Off)
        self.window.iptaliAyar.setIcon(icon)
        self.window.iptaliAyar.setIconSize(QSize(20, 20))
        self.window.tamamAyar.clicked.connect(self.tamamdirAyar)
        self.window.iptaliAyar.clicked.connect(lambda: self.window.stacked.setCurrentIndex(0))
        self.window.stil.addItem("Standart")

        for file in os.listdir("./icons"):
            if file.endswith(".qss"):
                self.window.stil.addItem(file.split(".")[0])
        self.window.lineEdit_1.setText(self.ayarlar["ftp"][0])
        self.window.lineEdit_2.setText(self.ayarlar["ftp"][1])
        self.window.lineEdit_3.setText(self.ayarlar["ftp"][2])
        self.window.lineEdit_4.setText(self.ayarlar["ftp"][3])
        self.window.stil.setCurrentText(self.ayarlar["stil"])
        self.window.stil.currentTextChanged.connect(self.stilkaydet)

        if self.ayarlar["arkaplan"][1]:
            self.window.checkBox.setCheckState(Qt.Checked)
        else:
            self.window.checkBox.setCheckState(Qt.Unchecked)
        self.window.sabit.setToolTip(QCoreApplication.translate("Dialog", u"\u0130lgili Saatte Oynayacak Reklam Yoksa G\u00f6sterilecek Video", None))
        self.window.arkaplan.setToolTip(QCoreApplication.translate("Dialog", u"\u0130ki Video Aras\u0131nda Arka Planda G\u00f6sterilecek Resim", None))
        self.window.checkBox.setToolTip(QCoreApplication.translate("Dialog", u"T\u0131kl\u0131ysa Arka Planda Se\u00e7ili Resim G\u00f6sterilir,\n"
"T\u0131kl\u0131 De\u011filse Arka Plan D\u00fcz Siyaht\u0131r.", None))
        self.window.tamamAyar.setIcon(QIcon("./icons/ok.png"))
        self.window.iptaliAyar.setIcon(QIcon("./icons/cancel.png"))
        self.window.iptaliAyar.setText("ÇIKIŞ")
        self.window.tamamAyar.setText("KAYDET")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.window.cihazlar.sizePolicy().hasHeightForWidth())
        self.window.cihazlar.setSizePolicy(sizePolicy)
        self.window.cihazlar.setMinimumSize(QSize(0, 300))
        self.window.cihazlar.setMaximumSize(QSize(16777215, 300))
        self.window.cihazlar.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.window.cihazlar.setShowGrid(True)
        self.window.cihazlar.setSelectionBehavior(QAbstractItemView.SelectRows)


        self.window.cihazlar.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.window.cihazlar.itemClicked.connect(self.listItemClickedCihazlar)
        self.window.cihazlar.itemDoubleClicked.connect(self.listItemDoubleClickedCihazlar)

        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.window.gorevlerCihaz.sizePolicy().hasHeightForWidth())
        self.window.gorevlerCihaz.setSizePolicy(sizePolicy1)
        self.window.gorevlerCihaz.setMinimumSize(QSize(355, 0))
        self.window.gorevlerCihaz.setMaximumSize(QSize(355, 16777215))
        self.window.gorevlerCihaz.setColumnCount(1)
        self.window.gorevlerCihaz.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.window.gorevlerCihaz.setShowGrid(True)
        self.doldurCihazlar()

        koor=self.window.cihazlar.item(0,2).text().split(",")
        if "None" not in koor:
            gmap1 = gmplot.GoogleMapPlotter(float(koor[0]),float(koor[1]), 15 )
            gmap1.apikey = "AIzaSyAJDWfFB3sg-gA1Es94ChZhmmUvVt6nT-s"
            gmap1.marker(float(koor[0]),float(koor[1]), color='darkred',title=self.window.cihazlar.item(0,1).text() )
            # Pass the absolute path
            gmap1.draw( "map11.html" )
        url = QtCore.QUrl.fromLocalFile(os.getcwd()+"/map11.html")
        self.my_web = QWebEngineView()
        self.my_web.load(url)
        self.window.horizontalLayout_4.addWidget(self.my_web)
        self.window.cihazlar.setHorizontalHeaderLabels(["ID","AÇIKLAMA","KONUM","IP","DURUM"])
        header = self.window.cihazlar.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Fixed)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        self.window.cihazlar.setColumnWidth(0, 100)
        self.window.cihazlar.setColumnWidth(1, 100)
        self.window.cihazlar.setColumnWidth(2, 100)
        self.window.cihazlar.setColumnWidth(3, 100)
        self.window.gorevlerCihaz.setHorizontalHeaderLabels(["GÖREVLER"])
        header = self.window.cihazlar.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Fixed)
        self.window.gorevlerCihaz.setColumnWidth(0, 345)
        self.window.gorevlerCihaz.verticalHeader().setVisible(False)


        self.doldurgorev(self.window.cihazlar.item(0,0).text())
        self.tasima=QtWidgets.QLabel("Görevlere Dön")

        self.tasima.installEventFilter(self)
        self.window.statusBar().addPermanentWidget(self.tasima)
        self.window.stacked.currentChanged.connect(self.degisti)
        self.window.show()
        self.baslat()
    def degisti(self):
        if self.window.stacked.currentIndex() != 8:
            self.playButton.click()
    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton :
                self.window.stacked.setCurrentIndex(0)
        return QtCore.QObject.event(obj, event)
    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())
    def doldurCihazlar(self):

        mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )
        try:

            mySql_select_query = """select id,aciklama,ST_X(konum),ST_Y(konum),ip from cihazlar"""
            cursor = mydb.cursor()
            cursor.execute(mySql_select_query)
            myresult = cursor.fetchall()
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        kontroledilecek=[]
        for result in myresult:
            self.window.cihazlar.setRowCount(self.window.cihazlar.rowCount()+1)
            self.window.cihazlar.setItem(self.window.cihazlar.rowCount()-1,0,QtWidgets.QTableWidgetItem(result[0]))
            self.window.cihazlar.setItem(self.window.cihazlar.rowCount()-1,1,QtWidgets.QTableWidgetItem(result[1]))
            self.window.cihazlar.setItem(self.window.cihazlar.rowCount()-1,2,QtWidgets.QTableWidgetItem(str(result[2])+","+str(result[3])))
            self.window.cihazlar.setItem(self.window.cihazlar.rowCount()-1,3,QtWidgets.QTableWidgetItem(result[4]))
            self.window.cihazlar.setItem(self.window.cihazlar.rowCount()-1,4,QtWidgets.QTableWidgetItem("KONTROL EDİLMEDİ"))
        mydb.disconnect()


    async def kontrolet(self,gelen):
        work_queue = asyncio.Queue()
        for i in gelen:
            await work_queue.put(i)

        await asyncio.gather(
            asyncio.create_task(self.kontrol(work_queue)),
            )

    def doldurgorev(self,gelen):
        for saat, deger in self.saatler.items():
            self.saatler[saat]=[]
        for i in range(self.window.gorevlerCihaz.rowCount()):
            self.window.gorevlerCihaz.removeRow(0)
        mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )
        try:

            mySql_select_query = """select oynayan_gorev from ayarlar"""
            cursor = mydb.cursor()
            cursor.execute(mySql_select_query)
            myresult = cursor.fetchall()
            cursor.close()
            oynayan_gorev=myresult[0]

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        try:

            mySql_select_query = """select * from reklamlar where gorev=%s"""
            cursor = mydb.cursor()
            cursor.execute(mySql_select_query,(oynayan_gorev[0],))
            myresult = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        finally:
            mydb.disconnect()
        for result in myresult:

            if str(gelen) in result[3].strip().split(" "):
                eklenecek=result[4].split(" ")

                for saat in eklenecek:
                    ek=result[2].split("/")
                    ek=ek[len(ek)-1]
                    #ek=ek[:len(ek)-2]
                    self.saatler[saat]=self.saatler[saat]+[ek]
        sirali=sorted(self.saatler.items())
        for i in sirali:
            self.window.gorevlerCihaz.setRowCount(self.window.gorevlerCihaz.rowCount()+1)
            self.window.gorevlerCihaz.setItem(self.window.gorevlerCihaz.rowCount()-1,0,QtWidgets.QTableWidgetItem(i[0]))
            self.window.gorevlerCihaz.item(self.window.gorevlerCihaz.rowCount()-1,0).setTextAlignment(Qt.AlignCenter)
            self.window.gorevlerCihaz.item(self.window.gorevlerCihaz.rowCount()-1,0).setBackgroundColor(Qt.gray)
            for j in i[1]:
                self.window.gorevlerCihaz.setRowCount(self.window.gorevlerCihaz.rowCount()+1)
                self.window.gorevlerCihaz.setItem(self.window.gorevlerCihaz.rowCount()-1,0,QtWidgets.QTableWidgetItem(j))
    def listItemDoubleClickedCihazlar(self, QPos):
        subprocess.run(["C:\\Program Files\\RealVNC\\VNC Viewer\\vncviewer.exe", "-UserName=pi", self.window.cihazlar.item(self.window.cihazlar.currentRow(),3).text()])

    async def kontrol(self,geleni):
        while not geleni.empty():
            QtWidgets.qApp.processEvents()
            gelen = await geleni.get()

            response_list =ping(gelen[0],count=1, timeout=0.5)

            if "Reply" in str(response_list):
                self.window.cihazlar.setItem(gelen[1],4,QtWidgets.QTableWidgetItem("AÇIK"))
            else:
                self.window.cihazlar.setItem(gelen[1],4,QtWidgets.QTableWidgetItem("KAPALI"))

    def listItemClickedCihazlar(self, QPos):
        self.doldurgorev(self.window.cihazlar.item(self.window.cihazlar.currentRow(),0).text())
        koor=self.window.cihazlar.item(self.window.cihazlar.currentRow(),2).text().split(",")
        if "None" not in koor:
            gmap1 = gmplot.GoogleMapPlotter(float(koor[0]),float(koor[1]), 15 )
            gmap1.apikey = "AIzaSyAJDWfFB3sg-gA1Es94ChZhmmUvVt6nT-s"
            gmap1.marker(float(koor[0]),float(koor[1]), color='darkred',title=self.window.cihazlar.item(self.window.cihazlar.currentRow(),1).text() )
            # Pass the absolute path
            gmap1.draw( "map11.html" )
            url = QtCore.QUrl.fromLocalFile(os.getcwd()+"/map11.html")
            self.my_web.load(url)

    def stilkaydet(self):
        self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )


        try:
            mySql_insert_query = """update `ayarlar` set `stil`=%s """
            val=(self.window.stil.currentText(),)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_insert_query,val)
            self.mydb.commit()
            cursor.close()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Stil Değiştirilemedi.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        finally:
            self.mydb.disconnect()
            self.ayarlar["stil"]=self.window.stil.currentText()
            self.style_string=""
            try:
                with open("./icons/" + self.ayarlar["stil"] + ".qss","r") as file:
                    data = file.read()
                for dat in data:
                    self.style_string=self.style_string + dat
            except:
                pass
            self.window.setStyleSheet(self.style_string)

    def tamamdirAyar(self):
        self.ayarlar["ftp"]=[self.window.lineEdit_1.text(),self.window.lineEdit_2.text(),self.window.lineEdit_3.text(),self.window.lineEdit_4.text()]
        if self.window.checkBox.checkState()==Qt.Checked:
            self.ayarlar["arkaplan"][1]=True
        else:
            self.ayarlar["arkaplan"][1]=False

        self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )


        try:
            mySql_insert_query = """update `ayarlar` set `ftpsunucu`=%s,`ftpuser`=%s, `ftppass`=%s, `ftpdizin`=%s, `arkaplan`=%s """
            val=(self.ayarlar["ftp"][0],self.ayarlar["ftp"][1],self.ayarlar["ftp"][2],self.ayarlar["ftp"][3],self.ayarlar["arkaplan"][1],)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_insert_query,val)
            self.mydb.commit()
            cursor.close()

        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Ayarlar kaydedilemedi.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        finally:
            self.mydb.disconnect()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Ayarlar Kaydedildi.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        self.window.stacked.setCurrentIndex(0)
    def yuklesabit(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(None,"Sabit Dosyasını Seç", "./videolar/","mp4 Dosyaları (*.mp4)", options=options)

        ftp = FTP(self.ayarlar["ftp"][0])
        ftp.login (self.ayarlar["ftp"][1],self.ayarlar["ftp"][2])
        ftp.timeout=15
        ftp.cwd(self.ayarlar["ftp"][3]+"/sabit/")
        #self.window.statusBar().showMessage("Yükleniyor lütfen bekleyiniz..")
        file_path = Path(self.fileName)
        file = open(file_path, 'rb')
        try:
            ftp.storbinary(f'STOR {file_path.name}', file, blocksize=128)
            try:
                self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )
                mySql_insert_query = """update `ayarlar` set `sabitdosya`=%s"""
                val=(os.path.basename(self.fileName),)
                cursor = self.mydb.cursor()
                cursor.execute(mySql_insert_query,val)
                self.mydb.commit()
                cursor.close()
            except mysql.connector.Error as error:

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText ("Sabit Dosya Veritabanına kaydedilemedi.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            finally:
                self.mydb.disconnect()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Dosya yüklenemedi.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        finally:
            ftp.close()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Yükleme tamamlandı.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
    def yuklearkaplan(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(None,"Arka Plan Dosyasını Seç", "./","png Dosyaları (*.png)", options=options)
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_insert_query = """update `ayarlar` set `arkaplandosya`=%s"""
            val=(os.path.basename(self.fileName),)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_insert_query,val)
            self.mydb.commit()
            cursor.close()
        except mysql.connector.Error as error:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Arkaplan veritabanına kaydedilemedi..")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        finally:
            self.mydb.disconnect()
        ftp = FTP(self.ayarlar["ftp"][0])
        ftp.login (self.ayarlar["ftp"][1],self.ayarlar["ftp"][2])
        ftp.timeout=15
        ftp.cwd(self.ayarlar["ftp"][3]+"/sabit/")
        #self.window.statusBar().showMessage("Yükleniyor lütfen bekleyiniz..")
        file_path = Path(self.fileName)
        file = open(file_path, 'rb')
        try:
            ftp.storbinary(f'STOR {file_path.name}', file, blocksize=128)
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Dosya Yüklenemedi.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        ftp.close()

    def combo_secGrup(self):
        grups=self.gruplar[self.window.combo.currentText()]
        self.window.lineEdit.setText(self.window.combo.currentText())
        for i in range(self.window.listid.count()):

            if self.window.listid.item(i).text().split("\t")[0] in grups:

                self.window.listid.item(i).setCheckState(QtCore.Qt.Checked)
            else:
                self.window.listid.item(i).setCheckState(QtCore.Qt.Unchecked)
    def silDefGrup(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText ("Grubu Silmek İstediğinize Emin misiniz?")
        msg.setStyleSheet(self.style_string)
        msg.setWindowTitle("Uyarı")

        msg.setStandardButtons(QtWidgets.QMessageBox.Ok  | QtWidgets.QMessageBox.Cancel)
        #msg.buttonClicked.connect(self.msgbtn)
        retval = msg.exec_()
        if retval==1024 and self.window.combo.currentText() !="Seçiniz veya Yeni İsim Giriniz":
            try:

                mySql_delete_query = """delete from `gruplar` where grup=%s; """
                val=(self.window.combo.currentText(),)
                cursor = self.mydb.cursor()
                cursor.execute(mySql_delete_query,val)
                self.mydb.commit()
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)

                msg.setText ("Grup silindi.")

                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok )
                #msg.buttonClicked.connect(self.msgbtn)
                msg.exec_()


                cursor.close()
                self.gruplarial()
            except mysql.connector.Error as error:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)

                msg.setText ("Grup silinemedi. Böyle bir grup yok.")
                msg.setStyleSheet(self.style_string)
                msg.setWindowTitle("Uyarı")

                msg.setStandardButtons(QtWidgets.QMessageBox.Ok )
                #msg.buttonClicked.connect(self.msgbtn)
                msg.exec_()

                return

        else:
            pass
    def tamamdirGrup(self):
        if self.window.lineEdit.text() == "":
            return
        self.mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )
        try:

            mySql_select_query = """select grup from gruplar where grup= %s"""
            val=(self.window.lineEdit.text(),)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query,val)

            myresult = cursor.fetchall()
            cursor.close()
            idler=[]
            for i in range(self.window.listid.count()):

                if self.window.listid.item(i).checkState()==QtCore.Qt.Checked:
                    idler.append(self.window.listid.item(i).text().split("\t")[0])
            if len(myresult)==0:

                try:

                    mySql_insert_query = """INSERT INTO `gruplar` (`sira`, `grup`, `elemanlar`) VALUES (NULL, %s,%s); """
                    val=(self.window.lineEdit.text(),str(idler),)
                    cursor = self.mydb.cursor()
                    cursor.execute(mySql_insert_query,val)
                    self.mydb.commit()
                    self.gruplarial()
                    print(cursor.rowcount, "Record inserted successfully into Laptop table")
                    cursor.close()

                except mysql.connector.Error as error:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText ("ID'ler kaydedilemedi.")
                    msg.setWindowTitle("Uyarı")
                    msg.setStyleSheet(self.style_string)
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    return
            else:
                try:
                    mySql_insert_query = """UPDATE gruplar
                    SET elemanlar = %s
                    WHERE grup = %s; """
                    val=(str(idler),self.window.lineEdit.text(),)
                    cursor = self.mydb.cursor()
                    cursor.execute(mySql_insert_query,val)
                    self.mydb.commit()
                    print(cursor.rowcount, "Record updated successfully into Laptop table")
                    self.gruplar[self.lineEdit.text()]=idler
                    cursor.close()
                    self.gruplarial()
                except mysql.connector.Error as error:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText ("ID'ler kaydedilemedi.")
                    msg.setWindowTitle("Uyarı")
                    msg.setStyleSheet(self.style_string)
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    return

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))

    def gruplarial(self):
        self.gruplar= dict()
        try:

            mySql_select_query = """select * from gruplar"""
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query)
            myresult = cursor.fetchall()
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        finally:
            self.mydb.disconnect()
        for result in myresult:
            #result[2] veritabanında text olarak tutuluyor. o yüzden liste çeviriyorum.
            self.gruplar[result[1]]=ast.literal_eval(result[2])

    def doldurIDler(self):
        self.window.listWidget_2.clear()
        idler = []
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_select_query = """select * from cihazlar"""
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query)
            myresult = cursor.fetchall()
            cursor.close()

        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        finally:
            self.mydb.disconnect()
        for result in myresult:
            idler.append([result[1] , result[2]])
        for i in idler:
            item = QListWidgetItem()
            item.setText(i[0] + "\t" + i[1])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Checked)
            self.window.listWidget_2.addItem(item)
    def doldurlistid(self):
                for key in self.gruplar:
                    self.window.combo.addItem(key)
                idler = []
                self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )
                try:
                    mySql_select_query = """select * from cihazlar"""
                    cursor = self.mydb.cursor()
                    cursor.execute(mySql_select_query)
                    myresult = cursor.fetchall()
                    cursor.close()

                except mysql.connector.Error as error:
                    print("Failed to insert record into Laptop table {}".format(error))

                for result in myresult:
                    idler.append([result[1] , result[2]])
                self.window.listid.clear()
                for i in idler:
                    item = QListWidgetItem()
                    item.setText(i[0] + "\t" + i[1])
                    item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.Checked)
                    self.window.listid.addItem(item)
    def ipmi(self,address):
        try:
            socket.inet_pton(socket.AF_INET, address)
        except AttributeError:  # no inet_pton here, sorry
            try:
                socket.inet_aton(address)
            except socket.error:
                return False
            return address.count('.') == 3
        except socket.error:  # not a valid address
            return False
        return True

    def eklemeCihaz(self):
        kontrol=True
        mesaj=""
        if not self.ipmi(self.window.txtip.text()):
            mesaj=mesaj + "\n" + "IP adresi uygun değil."
            kontrol=False
        if self.window.txtId.text()=="":
            mesaj=mesaj + "\n" + "ID numarası boş olamaz."
            kontrol=False
        try:
            int(self.window.txtId.text())
        except:
            mesaj=mesaj + "\n" + "ID numarası tam sayı olmalıdır."
            kontrol=False
        try:
            float(self.window.txtx.text())
        except:
            mesaj=mesaj + "\n" + "Konumun X koordinatı float (noktalı sayı) olmalıdır."
            kontrol=False
        try:
            float(self.window.txty.text())
        except:
            mesaj=mesaj + "\n" + "Konumun Y koordinatı float (noktalı sayı) olmalıdır."
            kontrol=False
        if self.window.txtAciklama.text()=="":
            mesaj=mesaj + "\n" + "Açıklama boş olamaz."
            kontrol=False
        if not kontrol:
            print ("aşağıdaki bilgileri düzeltip tekrar ekle butonunu tıklayınız.")
            print(mesaj)
            return

        self.mydb = mysql.connector.connect(
          host="213.238.178.192",
          user="root",
          passwd="root_password",
          database="reklam"
        )
        mySql_insert_query = """select id from cihazlar where id= %s """
        val=(self.window.txtId.text(),)
        cursor = self.mydb.cursor()
        cursor.execute(mySql_insert_query,val)
        cursor.fetchall()
        if cursor.rowcount>0:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText ("Bu ID mevcuttur. Üzerine yazmak için Tamam'ı, yeni ID girmek için İptal'i tıklayın.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok  | QtWidgets.QMessageBox.Cancel)
            retval = msg.exec_()
            if retval==1024:
                try:
                    self.mydb = mysql.connector.connect(
                      host="213.238.178.192",
                      user="root",
                      passwd="root_password",
                      database="reklam"
                    )
                    mySql_insert_query = """update cihazlar set aciklama=%s, konum=GeomFromText('POINT(%s %s)'),ip=%s where id=%s  """
                    val=(self.window.txtAciklama.text(),float(self.window.txtx.text()),float(self.window.txty.text()),self.window.txtip.text(),self.window.txtId.text(),)
                    cursor = self.mydb.cursor()
                    cursor.execute(mySql_insert_query,val)
                    self.mydb.commit()
                    cursor.close()
                    self.window.txtAciklama.setText("")
                    self.window.txtId.setText("")
                    self.window.txtip.setText("")
                    self.window.txtx.setText("")
                    self.window.txty.setText("")
                    return
                except mysql.connector.Error as error:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText ("Görev kaydedilemedi.")
                    msg.setWindowTitle("Uyarı")
                    msg.setStyleSheet(self.style_string)
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msg.exec_()
                    return
            else:
                return
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            self.window.idlist.addItem(self.window.txtId.text() + "\t" + self.window.txtAciklama.text())
            mySql_insert_query = """INSERT INTO `cihazlar` (`sira`, `id`, `aciklama`,`konum`, `ip`) VALUES (NULL, %s,%s, GeomFromText('POINT(%s %s)'),%s); """
            val=(self.window.txtId.text(),self.window.txtAciklama.text(),float(self.window.txtx.text()),float(self.window.txty.text()),self.window.txtip.text(),)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_insert_query,val)
            self.mydb.commit()
            self.window.txtAciklama.setText("")
            self.window.txtId.setText("")
            self.window.txtip.setText("")
            self.window.txtx.setText("")
            self.window.txty.setText("")
            cursor.close()
        except mysql.connector.Error as error:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Information)
            msg.setText ("ID'ler kaydedilemedi.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg.exec_()
            return


    def tiklandiCihaz(self):
        id=self.window.idlist.item(self.window.idlist.currentRow()).text().split("\t")[0]
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_select_query = """select id,aciklama,ST_X(konum),ST_Y(konum),ip from cihazlar where id=%s"""
            val=(id,)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query,val)
            result = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        self.window.txtId.setText(result[0][0])
        self.window.txtAciklama.setText(result[0][1])
        self.window.txtx.setText(str(result[0][2]))
        self.window.txty.setText(str(result[0][3]))
        self.window.txtip.setText(result[0][4])

    def menuItemClickedCihaz(self):
        currentItemName=str(self.window.idlist.currentItem().text())
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText ("Listeden Silmek İstediğinize Emin misiniz?")
        msg.setWindowTitle("Uyarı")
        msg.setStyleSheet(self.style_string)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok  | QtWidgets.QMessageBox.Cancel)

        retval = msg.exec_()
        if retval==1024:
            listItems=self.window.idlist.selectedItems()
            if not listItems: return
            id=self.window.idlist.currentItem().text().split("\t")[0]
            try:
                self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )
                mySql_delete_query = """delete from `cihazlar` where id=%s; """
                val=(id,)
                cursor = self.mydb.cursor()
                cursor.execute(mySql_delete_query,val)
                self.mydb.commit()
                print(cursor.rowcount, "Record inserted successfully into Laptop table")
                cursor.close()
            except mysql.connector.Error as error:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText ("ID'ler kaydedilemedi.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.exec_()
                return
            for i in range(self.window.idlist.count()):
               self.window.idlist.takeItem(0)
            self.doldurCihaz()
    def listItemRightClickedCihaz(self, QPos):
        self.listMenu= QtWidgets.QMenu()
        menu_item = self.listMenu.addAction("Cihazı Sil")
        self.listMenu.connect(menu_item, QtCore.SIGNAL("triggered()"), self.menuItemClickedCihaz)
        parentPosition = self.window.idlist.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def doldurCihaz(self):
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_select_query = """select * from cihazlar"""
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query)
            myresult = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        for result in myresult:
            self.window.idlist.addItem(result[1] + "\t" + result[2])



    def ac(self):
        self.window.stacked.setCurrentIndex(1)
        self.doldurGorev(0)

    def tamamGorev(self):
        self.show_gorevyuk(self.window.gorevler.currentItem().text())
        self.window.stacked.setCurrentIndex(0)

    def show_gorevyuk(self, gorev):
        for i in range(self.window.tablo.rowCount()):
            self.window.tablo.removeRow(0)
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_select_query = """select * from reklamlar where gorev= %s """

            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query,(gorev,))
            myresult = cursor.fetchall()
            cursor.close()
        except mysql.connector.Error as error:
            print("Hata",error)
        finally:
            self.mydb.disconnect()
        for result in myresult:
            self.tabloyaYaz([result[3],result[4],result[2]])

    def tabloyaYaz(self,gelen):
        grup = QtWidgets.QHBoxLayout()
        grup.setObjectName("horizontalLayout")
        grup.setSpacing(0)
        grup.setContentsMargins(0,0,0,0)
        buton1 = QtWidgets.QPushButton()
        buton1.setText("")
        buton1.setToolTip("Görevi Sil")
        buton1.setIcon(QIcon("./icons/removetask.png"))
        buton1.setFixedSize(QSize(30,30))
        buton1.setFlat(True)
        buton1.clicked.connect(self.menuItemClicked)

        buton2 = QtWidgets.QPushButton()
        buton2.setText("")
        buton2.clicked.connect(self.gorevgosterClicked)
        buton2.setIcon(QIcon("./icons/refresh.png"))
        buton2.setFixedSize(QSize(30,30))
        buton2.setFlat(True)
        buton2.setToolTip("Görevi Düzenle")

        buton3 = QtWidgets.QPushButton()
        buton3.setText("")
        buton3.clicked.connect(self.videoizle)
        buton3.setIcon(QIcon("./icons/watch.png"))
        buton3.setFixedSize(QSize(30,30))
        buton3.setFlat(True)
        buton3.setToolTip("Görevi İzle")

        grup.addWidget(buton1)
        grup.addWidget(buton2)
        grup.addWidget(buton3)



        cellWidget = QtWidgets.QWidget()
        cellWidget.setLayout(grup)


        if len(gelen)==3:
            self.window.tablo.setRowCount(self.window.tablo.rowCount()+1)
            self.window.tablo.setItem(self.window.tablo.rowCount()-1,0,QtWidgets.QTableWidgetItem(gelen[2]))
            self.window.tablo.setItem(self.window.tablo.rowCount()-1,1,QtWidgets.QTableWidgetItem(gelen[0]))
            self.window.tablo.setItem(self.window.tablo.rowCount()-1,2,QtWidgets.QTableWidgetItem(gelen[1]))
            self.window.tablo.setCellWidget(self.window.tablo.rowCount()-1,3,cellWidget)
        else:
            self.window.tablo.setItem(int(gelen[3]),0,QtWidgets.QTableWidgetItem(gelen[2]))
            self.window.tablo.setItem(int(gelen[3]),1,QtWidgets.QTableWidgetItem(gelen[0]))
            self.window.tablo.setItem(int(gelen[3]),2,QtWidgets.QTableWidgetItem(gelen[1]))

    def doldurGorev(self,gelen):
        self.window.gorevler.clear()
        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_select_query = """select DISTINCT gorev from reklamlar where durum=%s"""

            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query,(gelen,))
            myresult = cursor.fetchall()

        except:
            print("hata")
        finally:
            self.mydb.disconnect()
        for result in myresult:
            self.window.gorevler.addItem(result[0])
        cursor.close()

    def toggleRadio(self):
        rdButon=self.sender()
        if rdButon.text()=="Kaydedilmiş görevler":
            self.doldurGorev(0)
        else:
            self.doldurGorev(1)

    def cikis(self):
        app.quit()

    def gorevgosterClicked(self):
        p = self.sender().parent()
        y=p.pos().y()
        it = self.window.tablo.itemAt(QtCore.QPoint(100,y))
        i = self.window.tablo.row(it)
        gidecek=[i,self.window.tablo.item(i,0).text(),self.window.tablo.item(i,1).text(),self.window.tablo.item(i,2).text()]
        self.gorev_ekleGoster(gelen=gidecek)

    def menuItemClicked(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText ("Görevi Silmek İstediğinize Emin misiniz?")
        msg.setStyleSheet(self.style_string)
        msg.setWindowTitle("Uyarı")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok  | QtWidgets.QMessageBox.Cancel)

        retval = msg.exec_()
        if retval==1024:
            p = self.sender().parent()
            y=p.pos().y()
            it = self.window.tablo.itemAt(QtCore.QPoint(100,y))
            row = self.window.tablo.row(it)
            self.window.tablo.removeRow(row)


    def videoizle(self):
        p = self.sender().parent()
        y=p.pos().y()
        it = self.window.tablo.itemAt(QtCore.QPoint(100,y))
        row = self.window.tablo.row(it)
        self.fileName=self.window.tablo.item(row,0).text()
        self.window.stacked.setCurrentIndex(8)
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(self.fileName)))
        self.playButton.setEnabled(True)
        self.playButton.click()

    def cihaz_ekleGoster(self):
        self.window.stacked.setCurrentIndex(4)

    def ayar(self):
        self.window.stacked.setCurrentIndex(6)
    def grup_ekleGoster(self):
        self.doldurlistid()
        self.window.stacked.setCurrentIndex(5)

    def gorev_ekleGoster(self,gelen=""):
        self.doldurIDler()
        self.gelen=gelen
        self.window.stacked.setCurrentIndex(2)
        self.window.label_5.setText("")

        if self.gelen!="":

            self.window.label_5.setText(self.gelen[1])
            idler=self.gelen[2]

            zaman=self.gelen[3]
            ids=idler.split(" ")
            zamanlar= zaman.split(" ")
            for index in range(self.window.listWidget_2.count()):
                item = self.window.listWidget_2.item(index)


                if item.text().split("\t")[0] in ids:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)

            for index in range(self.window.listWidget.count()):
                item = self.window.listWidget.item(index)
                if item.text() in zamanlar:
                    item.setCheckState(QtCore.Qt.Checked)
                else:
                    item.setCheckState(QtCore.Qt.Unchecked)


        if self.gelen=="":
            self.window.tamam.setText(QtWidgets.QApplication.translate("Dialog", "TAMAM", None, -1))
        else:
            self.window.tamam.setText(QtWidgets.QApplication.translate("Dialog", "GÜNCELLE", None, -1))


    def secim(self):

        if self.window.hepsini.isChecked():
            for index in range(self.window.listWidget.count()):
                item = self.window.listWidget.item(index)
                item.setCheckState(QtCore.Qt.Checked)
                self.window.hepsini.setText("Hepsini Kaldır")
        else:
            for index in range(self.window.listWidget.count()):
                item = self.window.listWidget.item(index)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.window.hepsini.setText("Hepsini Seç")

    def ekleme(self):

        if self.window.label_5.text()=="":
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Lütfen Reklam Seçiniz.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        idler=""
        for index in range(self.window.listWidget_2.count()):
            item = self.window.listWidget_2.item(index)
            if item.checkState() == Qt.Checked:
                idler=idler + " " + item.text().split("\t")[0]
        zamanlar=""
        for index in range(self.window.listWidget.count()):
            item = self.window.listWidget.item(index)
            if item.checkState() == Qt.Checked:
                zamanlar= zamanlar + " " + item.text().split("\t")[0]
        if self.window.tamam.text()=="TAMAM":
            self.tabloyaYaz([idler,zamanlar,self.window.label_5.text()])
            self.window.stacked.setCurrentIndex(0)
        else:
            self.tabloyaYaz([idler,zamanlar,self.window.label_5.text(),self.gelen[0]])
            self.window.stacked.setCurrentIndex(0)


    def dosyaSec(self):

        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Dosya Seç", "./videolar/","mp4 Dosyaları (*.mp4)", options=options)

        if self.fileName:
            self.window.label_5.setText(self.fileName)

    def combo_sec(self):
        if self.window.cmbid.currentIndex()==0:
            for i in range(self.window.listWidget_2.count()):
                self.window.listWidget_2.item(i).setCheckState(QtCore.Qt.Checked)
        elif self.window.cmbid.currentIndex()==1:
            for i in range(self.window.listWidget_2.count()):
                self.window.listWidget_2.item(i).setCheckState(QtCore.Qt.Unchecked)
        else:
            for i in range(self.window.listWidget_2.count()):

                if self.window.listWidget_2.item(i).text().split("\t")[0] in self.gruplar[self.window.cmbid.currentText()]:

                    self.window.listWidget_2.item(i).setCheckState(QtCore.Qt.Checked)
                else:
                    self.window.listWidget_2.item(i).setCheckState(QtCore.Qt.Unchecked)

    def cihazGoster(self):
        self.window.stacked.setCurrentIndex(7)

    def duz(self,gelen):
        #türkçe karakterleri kaldırmak için kullandım. FTP coding sorunu çıkarıyor.
        gelen=gelen.replace("ı","i")
        gelen=gelen.replace("İ","I")
        gelen=gelen.replace("Ğ","G")
        gelen=gelen.replace("ğ","g")
        gelen=gelen.replace("Ü","U")
        gelen=gelen.replace("ü","u")
        gelen=gelen.replace("Ş","S")
        gelen=gelen.replace("ş","s")
        gelen=gelen.replace("Ö","O")
        gelen=gelen.replace("ö","o")
        gelen=gelen.replace("Ç","C")
        gelen=gelen.replace("ç","c")
        return gelen


    def tabloyaYaz(self,gelen):
        grup = QtWidgets.QHBoxLayout()
        grup.setObjectName("horizontalLayout")
        grup.setSpacing(0)
        grup.setContentsMargins(0,0,0,0)
        buton1 = QtWidgets.QPushButton()
        buton1.setText("")
        buton1.setToolTip("Görevi Sil")
        buton1.setIcon(QIcon("./icons/removetask.png"))
        buton1.setFixedSize(QSize(30,30))
        buton1.setFlat(True)
        buton1.clicked.connect(self.menuItemClicked)

        buton2 = QtWidgets.QPushButton()
        buton2.setText("")
        buton2.clicked.connect(self.gorevgosterClicked)
        buton2.setIcon(QIcon("./icons/refresh.png"))
        buton2.setFixedSize(QSize(30,30))
        buton2.setFlat(True)
        buton2.setToolTip("Görevi Düzenle")

        buton3 = QtWidgets.QPushButton()
        buton3.setText("")
        buton3.clicked.connect(self.videoizle)
        buton3.setIcon(QIcon("./icons/watch.png"))
        buton3.setFixedSize(QSize(30,30))
        buton3.setFlat(True)
        buton3.setToolTip("Görevi İzle")

        grup.addWidget(buton1)
        grup.addWidget(buton2)
        grup.addWidget(buton3)



        cellWidget = QtWidgets.QWidget()
        cellWidget.setLayout(grup)


        if len(gelen)==3:
            self.window.tablo.setRowCount(self.window.tablo.rowCount()+1)
            self.window.tablo.setItem(self.window.tablo.rowCount()-1,0,QtWidgets.QTableWidgetItem(gelen[2]))
            self.window.tablo.setItem(self.window.tablo.rowCount()-1,1,QtWidgets.QTableWidgetItem(gelen[0]))
            self.window.tablo.setItem(self.window.tablo.rowCount()-1,2,QtWidgets.QTableWidgetItem(gelen[1]))
            self.window.tablo.setCellWidget(self.window.tablo.rowCount()-1,3,cellWidget)
        else:
            self.window.tablo.setItem(int(gelen[3]),0,QtWidgets.QTableWidgetItem(gelen[2]))
            self.window.tablo.setItem(int(gelen[3]),1,QtWidgets.QTableWidgetItem(gelen[0]))
            self.window.tablo.setItem(int(gelen[3]),2,QtWidgets.QTableWidgetItem(gelen[1]))


    def uploadDef(self):
        if self.window.tablo.rowCount()==0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Yüklenecek görev yok. Lütfen görev ekleyiniz.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        if self.internet_on()==False:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("İnternet bağlantısı yok. Lütfen bağlantınızı kontrol ediniz.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return


        simdi=datetime.now()
        gorev=str(simdi.day)+"."+str(simdi.month)+"."+str(simdi.year)+"-"+str(simdi.hour)+":"+str(simdi.minute)+"."+str(simdi.second)

        line=[]
        #dosyalar FTP'ye yüklenecek türkçe karakterler kaldırılmış dosyaları tutuyor.
        #orjinal türkçe karakterler arındırılmamaış dosya isimlerini tutuyor.
        dosyala=[]
        dosyalar=[]
        for i in range(self.window.tablo.rowCount()):
            if not os.path.isfile(self.window.tablo.item(i,0).text()):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText ("Belirtilen dosya yok. Bu dosyaya işlem yapılmayacak.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                continue

            line.append(self.duz(self.window.tablo.item(i,0).text()) + "|" + self.window.tablo.item(i,1).text() + "|" +self.window.tablo.item(i,2).text().strip()+"\n")
            if self.duz(self.window.tablo.item(i,0).text()) not in dosyalar:
                dosyalar.append(self.duz(self.window.tablo.item(i,0).text()))
                dosyala.append(self.window.tablo.item(i,0).text())
            try:
                self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )
                mySql_insert_query = """INSERT INTO `reklamlar` (`sira`, `gorev`, `dosya`, `idler`, `zamanlar`, `zaman`, `durum`) VALUES (NULL, %s,%s,%s,%s, CURRENT_TIMESTAMP,True); """
                val=(gorev,self.duz(self.window.tablo.item(i,0).text()) , self.window.tablo.item(i,1).text() ,self.window.tablo.item(i,2).text().strip())
                cursor = self.mydb.cursor()
                cursor.execute(mySql_insert_query,val)
                self.mydb.commit()

                cursor.close()

            except mysql.connector.Error as error:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText ("Görev kaydedilemedi.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            finally:
                self.mydb.disconnect()
        self.progressBar.setMaximum(len(dosyalar))
        self.progressBar.setValue(0)
        self.progressBar.setVisible(True)
        self.progressBar2.setVisible(True)
        self.progressBar2.setValue(0)
        #tüm videolar FTP ye yükleniyor.
        ftp = FTP(self.ayarlar["ftp"][0])
        ftp.login (self.ayarlar["ftp"][1],self.ayarlar["ftp"][2])
        ftp.timeout=15
        ftp.cwd(self.ayarlar["ftp"][3])
        self.window.statusBar().showMessage("Yükleniyor lütfen bekleyiniz..")
        for i in range(len(dosyalar)):

            file_path = Path(dosyalar[i])
            file = open(dosyala[i], 'rb')
            self.progressBar2.setMaximum(os.path.getsize(dosyala[i]))
            self.progressBar2.setValue(0)
            try:

                ftp.storbinary(f'STOR {file_path.name}', file, blocksize=128, callback = self.handle)
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText ("Dosya yüklenemedi.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                self.progressBar.setVisible(False)
                self.progressBar2.setVisible(False)
                return

            self.progressBar2.setValue(self.progressBar2.maximum())
            self.progressBar.setValue(self.progressBar.value()+1)
            sleep(1)
        self.progressBar.setValue(self.progressBar.maximum())
        sleep(1)
        self.progressBar.setVisible(False)
        self.progressBar2.setVisible(False)
        ftp.close()

        if(len(dosyalar)>0):
            try:
                self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )
                mySql_insert_query = """update `ayarlar` set `oynayan_gorev`=%s  """
                val=(gorev,)
                cursor = self.mydb.cursor()
                cursor.execute(mySql_insert_query,val)
                self.mydb.commit()
                cursor.close()

            except mysql.connector.Error as error:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText ("Görev kaydedilemedi.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            finally:
                self.mydb.disconnect()
        self.window.statusBar().showMessage("Yükleme Tamamlandı")
        sleep(2)
        self.window.statusBar().showMessage("Hazır",0)



    def handle(self,block):
        self.progressBar2.setValue(self.progressBar2.value()+128)
        app.processEvents()

    def kaydetGorev(self):
        self.window.stacked.setCurrentIndex(3)
        self.window.tamamGorev.clicked.connect(self.kaydetDef)

    def kaydetDef(self):
        self.window.stacked.setCurrentIndex(3)
        if self.window.tablo.rowCount()==0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Kaydedilecek görev yok. Lütfen görev ekleyiniz.")
            msg.setWindowTitle("Uyarı")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return

        try:
            self.mydb = mysql.connector.connect(
              host="213.238.178.192",
              user="root",
              passwd="root_password",
              database="reklam"
            )
            mySql_select_query = """select gorev from reklamlar where gorev= %s """
            val=(self.window.gorevadi.text(),)
            cursor = self.mydb.cursor()
            cursor.execute(mySql_select_query,val)
            myresult = cursor.fetchall()
            if cursor.rowcount==0:
                self.kaydet_gorev([self.window.gorevadi.text()])
                return
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText ("Bu Görev ismi mevcuttur. Üzerine yazmak için Tamam'ı, yeni isim girmek için İptal'i tıklayın.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok  | QtWidgets.QMessageBox.Cancel)
                #msg.buttonClicked.connect(self.msgbtn)
                retval = msg.exec_()
                if retval==1024:
                    self.kaydet_gorev([self.window.gorevadi.text(),1])
                    return
                else:
                    return
            cursor.close()
        except mysql.connector.Error as error:
            print("Failed to insert record into Laptop table {}".format(error))
        finally:
            self.mydb.disconnect()
    def kaydet_gorev(self, gorev):
        if len(gorev)==1:
            for i in range(self.window.tablo.rowCount()):
                try:
                    self.mydb = mysql.connector.connect(
                      host="213.238.178.192",
                      user="root",
                      passwd="root_password",
                      database="reklam"
                    )
                    mySql_insert_query = """INSERT INTO `reklamlar` (`sira`, `gorev`, `dosya`, `idler`, `zamanlar`, `zaman`, `durum`) VALUES (NULL, %s,%s,%s,%s, CURRENT_TIMESTAMP,False); """
                    val=(gorev[0],self.duz(self.window.tablo.item(i,0).text()) , self.window.tablo.item(i,1).text() ,self.window.tablo.item(i,2).text().strip())
                    cursor = self.mydb.cursor()
                    cursor.execute(mySql_insert_query,val)
                    self.mydb.commit()
                    print(cursor.rowcount, "Record inserted successfully into Laptop table")
                    cursor.close()
                    if self.duz(self.window.tablo.item(i,0).text())!=self.window.tablo.item(i,0).text():
                        os.rename(self.window.tablo.item(i,0).text(),self.duz(self.window.tablo.item(i,0).text()))
                        self.window.tablo.item(i,0).setText(self.duz(self.window.tablo.item(i,0).text()))
                except mysql.connector.Error as error:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText ("Görev kaydedilemedi.")
                    msg.setWindowTitle("Uyarı")
                    msg.setStyleSheet(self.style_string)
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
                finally:
                    self.mydb.disconnect()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Görev kaydedildi.")
            msg.setWindowTitle("Bilgi")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif gorev[1]==1:
            try:
                self.mydb = mysql.connector.connect(
                  host="213.238.178.192",
                  user="root",
                  passwd="root_password",
                  database="reklam"
                )
                mySql_insert_query = """delete from reklamlar where gorev=%s """
                val=(gorev[0],)
                cursor = self.mydb.cursor()
                cursor.execute(mySql_insert_query,val)
                self.mydb.commit()
                print(cursor.rowcount, "Record deleted successfully into Laptop table")
                cursor.close()
            except mysql.connector.Error as error:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText ("Görev silinemedi.")
                msg.setWindowTitle("Uyarı")
                msg.setStyleSheet(self.style_string)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()
                return
            for i in range(self.window.tablo.rowCount()):
                try:

                    mySql_insert_query = """INSERT INTO `reklamlar` (`sira`, `gorev`, `dosya`, `idler`, `zamanlar`, `zaman`, `durum`) VALUES (NULL, %s,%s,%s,%s, CURRENT_TIMESTAMP,False); """
                    val=(gorev[0],self.duz(self.window.tablo.item(i,0).text()) , self.window.tablo.item(i,1).text() ,self.window.tablo.item(i,2).text().strip())
                    cursor = self.mydb.cursor()
                    cursor.execute(mySql_insert_query,val)
                    self.mydb.commit()
                    print(cursor.rowcount, "Record inserted successfully into Laptop table")
                    cursor.close()
                    if self.duz(self.window.tablo.item(i,0).text())!=self.window.tablo.item(i,0).text():
                        os.rename(self.window.tablo.item(i,0).text(),self.duz(self.window.tablo.item(i,0).text()))
                        self.window.tablo.item(i,0).setText(self.duz(self.window.tablo.item(i,0).text()))
                except mysql.connector.Error as error:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText ("Görev kaydedilemedi.")
                    msg.setWindowTitle("Uyarı")
                    msg.setStyleSheet(self.style_string)
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
            self.mydb.disconnect()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText ("Görev düzenlendi..")
            msg.setWindowTitle("Bilgi")
            msg.setStyleSheet(self.style_string)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    pencere = Giris()

    sys.exit(app.exec_())

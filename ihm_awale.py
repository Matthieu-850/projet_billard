from IHM import MonAppli

from PyQt5.QtCore import *
#from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit , QFormLayout, QAction
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow

class Window_Menu (QtWidgets.QMainWindow) :

    def __init__(self, *args, **kwargs):
        super(Window_Menu, self).__init__(*args, **kwargs)


        self.setWindowTitle("Entrez vos prénoms")  # titre de la fenetre
        self.setFixedSize(300, 185)  # taille de la fenetre

        self.text = QLabel(self)
        self.text.setFixedSize(30, 235)
        #self.text.move(10,10)
        #self.text.setText("Entrer noms")
        #
        # self.button_un_joueur = QtWidgets.QPushButton("Prénom du premier jouer", self)  # cree un bouton
        # self.button_un_joueur.setFixedSize(250, 30)  # taille du bouton
        # self.button_un_joueur.move(120, 50)  # position du bouton
        # self.button_un_joueur.clicked.connect(self.prenom1)  # ce qu'il se passe quand on appui sur le bouton
        #
        # self.button_deux_joueur = QtWidgets.QPushButton("Prénom du second joueur", self)  # cree un bouton
        # self.button_deux_joueur.setFixedSize(250, 30)  # taille du bouton
        # self.button_deux_joueur.move(120, 100)  # position du bouton
        # self.button_deux_joueur.clicked.connect(self.prenom2)

        self.button_valider = QtWidgets.QPushButton("Lancer la partie", self)  # cree un bouton
        self.button_valider.setFixedSize(150, 60)  # taille du bouton
        font = self.button_valider.font()  # lineedit current font
        font.setPointSize(20)  # change it's size
        self.button_valider.setFont(font)
        self.button_valider.setFont(QFont('Calibri', 12))
        self.button_valider.move(80, 200)  # position du bouton

        zoneCentrale = QWidget()

        pixmap = QtGui.QPixmap("image4.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        zoneCentrale.lower()
        zoneCentrale.stackUnder(self)
        zoneCentrale.setAutoFillBackground(True)
        zoneCentrale.setPalette(pal)

        # self.con = QtWidgets.QWidget(self.centralwidget)
        # self.con.setGeometry(QtCore.QRect(20, 20, 300, 251))
        # # self.con.setObjectName("con")

        self.prenom1 = QLineEdit(self)
        self.prenom1.move (15,50)
        self.prenom2 = QLineEdit(self)
        self.prenom2.move(20, 100)
        self.nb_tour = QLineEdit(self)
        self.nb_tour.move(20, 150)
        #
        self.layout = QFormLayout()
        self.layout.addRow("Prénom du joueur 1 ", self.prenom1)
        self.layout.addRow("Prénom du joueur 2", self.prenom2)
        self.layout.addRow("Nombre de coups", self.nb_tour)
        #zoneCentrale.setLayout(self.button_valider)

        self.layout.addWidget(self.button_valider)
        zoneCentrale.setLayout (self.layout)
        self.setCentralWidget(zoneCentrale)

        self.button_valider.clicked.connect(self.prenoms)  # ce qu'il se passe

        self.show()

    def prenom2 (self) :
        self.close()

    def prenoms (self) :
        p1 = self.prenom1.text()
        p2 = self.prenom2.text()
        nb = int (self.nb_tour.text())
        if nb <1 or type (nb) != int:
            #self.layout.addRow("Nombre de coups\nEntier positif !!", self.nb_tour)
            pass
        else :
            self.win_deux = MonAppli(p1,p2,nb)
            self.win_deux.show()
            print (p1, p2)
            self.close ()


if __name__ == "__main__" :

    app = QApplication([])
    win = Window_Menu()
    app.exec()




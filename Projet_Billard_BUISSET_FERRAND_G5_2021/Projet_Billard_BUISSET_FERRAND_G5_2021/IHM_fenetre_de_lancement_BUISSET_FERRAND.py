from IHM_Billard_BUISSET_FERRAND import JeuBillard

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

        pixmap = QtGui.QPixmap("arriere_plan_lancement.png")
        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        zoneCentrale = QWidget()
        zoneCentrale.lower()
        zoneCentrale.stackUnder(self)
        zoneCentrale.setAutoFillBackground(True)
        zoneCentrale.setPalette(pal)

        self.setWindowTitle("Entrez vos prénoms, et le nombre coups")
        self.setFixedSize(300, 185)

        self.bouton_valider = QtWidgets.QPushButton("Lancer la partie", self)  # on crée un bouton qui affichera 'Lancer la partie'
        self.bouton_valider.setFixedSize(150, 60)  # taille du bouton
        self.bouton_valider.setFont(QFont('Calibri', 12))   # type et taille de police
        self.bouton_valider.move(80, 200)  # position du bouton

        self.prenom1 = QLineEdit(self)
        self.prenom1.move (25,50)
        self.prenom2 = QLineEdit(self)
        self.prenom2.move(20, 100)
        self.nb_tour = QLineEdit(self)
        self.nb_tour.move(20, 150)

        self.layout = QFormLayout()

        self.titre1 = QLabel ("Prénom du joueur 1 ")
        self.titre1.setFixedSize(120,20)
        self.titre1.move(50,50)
        self.titre1.show()

        self.titre2 = QLabel("Prénom du joueur 2 ")
        self.titre2.setFixedSize(120, 20)
        self.titre2.move(50, 100)
        self.titre2.show()

        self.titre3= QLabel("Nombre de coups")
        self.titre3.setFixedSize(120, 20)
        self.titre3.move(50, 150)
        self.titre3.show()

        self.layout.addRow(self.titre1, self.prenom1)
        self.layout.addRow(self.titre2, self.prenom2)
        self.layout.addRow(self.titre3, self.nb_tour)

        #self.layout.setSizeConstraint(100)

        self.layout.addWidget(self.bouton_valider)
        zoneCentrale.setLayout (self.layout)
        self.setCentralWidget(zoneCentrale)

        self.bouton_valider.clicked.connect(self.initialisation)
        # lorsque l'on clique sur le bouton bouton_valider, la méthode initialisation est appelée

        self.show()


    def initialisation (self) :
        """
        Auteur : Elodie

        initialisation :
        recueille les les prénoms des joueurs et le nombre de coups qu'ils veulent jouer.
        Lance la fenêtre de jeu avec ces paramètres
        """
        p1 = self.prenom1.text()
        p2 = self.prenom2.text()
        nb = self.nb_tour.text()
        try :
            nb = int (nb)
            if nb > 1 :  # les joueurs ont entré une donnée adaptée
                self.win_deux = JeuBillard(p1, p2, nb)  # on va pouvoir lancer le jeu avec les paramètres fournis par les joueurs
                self.win_deux.show()                  # La fenêtre billard est lancée
                self.close()
            else :      # on ne peut faire un nombre de coup négatif
                self.titre3.setText('Nombre positif requis !')  #il va falloir changer la valeur de nb
                self.titre3.setFixedSize(125, 20)
                self.titre3.show()
        except ValueError :   # on ne peut faire un nombre de coup qui ne soit pas un nombre entier
            self.titre3.setText('Nombre requis !')   # il va falloir changer la valeur de nb
            self.titre3.show()


if __name__ == "__main__" :

    app = QApplication([])
    win = Window_Menu()
    app.exec()



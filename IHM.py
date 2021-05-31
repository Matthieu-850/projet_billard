import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
#from QPixmap import QMatrix
from interfaceBon import Ui_mainWindow
from projet_8 import Partie, Boule_blanche, Boule, Plateau
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit , QFormLayout, QAction, QFontComboBox
from PyQt5.QtGui import QFont
import numpy as np
import time


# l'approche par héritage simple de la classe QMainWindow (même type de notre fenêtre
# créée avec QT Designer. Nous configurons après l'interface utilisateur
# dans le constructeur (la méthode init()) de notre classe

class MonAppli(QtWidgets.QMainWindow):
    def __init__(self, p1 = "joueur 1",p2 = "joueur 2", nb = 10):
        super().__init__()
        self.joueurs = [p1,p2]
        self.nb_coups = nb
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        #self.ui2 = Ui_mainWindow2()
        #self.ui2.setupUi2(self)

        #self.ui2.setupUi(self)
        pixmap = QtGui.QPixmap("carambole_m.jpg")
        self.i = 0
        self.TEST = []
        self.t = 0
        self.T = []

        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.con.lower()
        self.ui.con.stackUnder(self)
        self.ui.con.setAutoFillBackground(True)
        self.ui.con.setPalette(pal)

        #zoneCentrale = QWidget()
        #nom = QLineEdit(self)
        #prenom = QLineEdit(self)
        #age = QLineEdit(self)
        #layout = QFormLayout()
        #layout.addRow("Votre nom", nom)
        #layout.addRow("Votre prénom", prenom)
        #layout.addRow("Votre âge", age)
        #zoneCentrale.setLayout(layout)
        #self.setCentralWidget(zoneCentrale)

        self.painter = QtGui.QPainter()
        qp = self.painter
        self.painter2 = QtGui.QPainter()
        self.ui.con.paintEvent = self.drawEcosysteme1

        self.hw =  self.ui.con.height()   ###701  # (y) hauteur du widget con, ie la table
        self.lw =  self.ui.con.width()   #1101# (x) largeur du widget
        print("selon les x",self.lw, "  selon les y", self.hw)

        self.bande_n, self.bande_o, self.bande_e, self.bande_s = 76.2, 76.2, 76.2, 68  # epaisseurs des bandes sur notre image de table
        self.ehfw, self.egfw = 10, 10  # ecart haut fenetre - widget, ecart gauche fenetre - widget
        self.by, self.bx = self.hw - self.bande_n - self.bande_s, self.lw - self.bande_e - self.bande_o  # taille du tapis, correspondent à self.bn et self.be dans la classe plateau

        self.distx, self.disty = 0,0

        self.table = Partie(self.nb_coups, 0.005, self.bx, self.by)
        for bal in self.table.plat :
            print (bal.r)
        self.xp, self.yp, self.xr, self.yr = self.table.plat[self.i % 2].x + 86.2, self.table.plat[
             self.i % 2].y + 86.2, 0, 0
        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[self.i % 2].x + 86.2, self.table.plat[
             self.i % 2].y + 86.2
        self.ui.con.update()

        self.ui.Bouton_Demarrer.clicked.connect(self.demarrer)
        self.ui.Bouton_Jouer.clicked.connect(self.jouer)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.processInputFile1)

        #self.demarrer()

        self.painter2.begin(self.ui.con)
        #self.table.plat.queue.dessinimage(self.painter2,self.table.plat.queue.alpha2, self.table.plat[self.i % 2].x, self.table.plat[self.i % 2].y)
        self.painter2.end()

        # label =  QLabel ("testtesttest", self.ui.label)
        # label.setIndent (20)
        # label.sizeHint()
        # self.ui.label.setMargin(10)
        # self.ui.label.setText("coucouuuuuuuuuuuu")
        #self.ui.label.show()

        #font = self.ui.label.font()  # lineedit current font
        #font.setPointSize(11)  # change it's size
        #self.ui.label.setFont(font)
        self.ui.label.setFont(QFont ('Calibri',12))
        #self.ui.label.setFixedWidth(3000)


        font = self.ui.label2.font()  # lineedit current font
        font.setPointSize(11)  # change it's size
        self.ui.label2.setFont(font)
        self.ui.label2.setFont(QFont('Helvetica', 10))

        self.ui.label.setText("Tour {}. \nC'est à {} de jouer.".format(self.table.c +1, self.joueurs [self.i % 2]))
        self.ui.label.show()

        self.ui.label2.setText("{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0], self.table.points[0]))
        self.ui.label2.show()

        qp.begin(self.ui.con)
        #self.table.plat.point.dessinimage(self.painter, self.table.plat[self.i % 2].x - 90, self.table.plat[self.i % 2].y - 88.2)
        qp.end()

    def demarrer(self):
        print("Demarrer")

        self.table = Partie(self.nb_coups, 0.005, self.bx, self.by)
        for bal in self.table.plat:
            print(bal.r)

        self.ui.label.setText("Nouvelle partie \nTour {}. \nC'est à {} de jouer.".format(self.table.c + 1, self.joueurs[self.i % 2]))
        self.ui.label.show()
        self.ui.label2.setText(
            "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0], self.table.points[0]))
        self.ui.label2.show()
        #self.table = Partie(3, 0.02,self.lw ,self.hw)  #self.ui.con.width(), self.ui.con.height()) # 971-20*2-80 # 621-40*2
        #print( "partie crée")
        #self.timer.start (200)
        self.xp, self.yp, self.xr, self.yr = self.table.plat[self.i % 2].x + 86.2, self.table.plat[
            self.i % 2].y + 86.2, 0, 0
        self.table.plat.queue.x, self.table.plat.queue.y = self.table.plat[self.i % 2].x + 86.2, self.table.plat[
             self.i % 2].y + 86.2
        self.ui.con.update()

    def jouer(self):  # un coup
        print("tour {}".format(self.table.c))
        self.ui.label.setText("tour {}".format(self.table.c))
        self.ui.label.show()
        if self.table.c < self.table.nb_coups:
            self.table.c += 1
            x1, y1, x2, y2 = self.table.plat[self.i % 2 - 1].x, self.table.plat[self.i % 2 - 1].y, self.table.plat[
                self.i % 2 - 2].x, self.table.plat[self.i % 2 - 2].y
            self.TEST = [x1, y1, x2, y2]  # liste contenant les positions de boules non tapees juste avant le coup

            print("c'est à {} de jouer".format(self.joueurs [self.i % 2]))
            self.ui.label.setText("Tour {}. \nC'est à {} de jouer.".format(self.table.c, self.joueurs[self.i % 2]))
            self.ui.label.show()
            self.ui.label2.setText("{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                               self.table.points[0]))
            self.ui.label2.show()
            self.T = np.array([1 for i in range(self.table.plat.n)])

            # Boule_blanche.impulsion(self.table.plat[self.i % 2], 35, 400)  # 1 boule blanche
            Boule_blanche.impulsion(self.table.plat[self.i % 2], self.table.plat.queue.alpha2, self.table.plat.queue.p)
            #print('implullllllllllllllllllllllllllllllllllllllllllllll', self.table.plat.queue.alpha2)
            self.t = 0
            self.posx, self.posy = [[] for i in range(self.table.plat.n)], [[] for i in
                                                                            range(
                                                                                self.table.plat.n)]  # pour garder en mémoire les positions passées
            for i in range(self.table.plat.n):
                self.posx[i].append(self.table.plat[i].x)
                self.posy[i].append(self.table.plat[i].y)

            self.timer.start(7)

        if self.table.c >= self.table.nb_coups -1:
            print("{} : {} points \n{} : {} points ".format(self.joueurs [1], self.table.points[1], self.joueurs[0], self.table.points[0]))
            self.ui.label.setText(
                "{} : {} points \n{} : {} points ".format(self.joueurs [1], self.table.points[1], self.joueurs[0], self.table.points[0]))
            self.ui.label.show()
            if self.table.points[0] != self.table.points[1]:
                if self.table.points[0] > self.table.points[1]:
                    g = 0
                else:
                    g = 1
                self.ui.label.setText(
                    "{} : {} points \n{} : {} points. \n{} a gagné ! Félicitations ! ".format(self.joueurs [1],
                        self.table.points[1], self.joueurs[0], self.table.points[0], self.joueurs[g]))
                print("Le joueur {} a gagné ! Félicitations !".format(g))
                self.ui.label.show()
                self.ui.label2.setText(
                    "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                self.table.points[0]))
                self.ui.label2.show()
            else:
                self.ui.label.setText(
                    "{} : {} points \n{} : {} points. \nEgalité ! Bravo à vous deux ! ".format(
                        self.joueurs[1], self.table.points[1], self.joueurs[0], self.table.points[0]))
                print("Egalité ! Bravo à vous deux !")
                self.ui.label.show()
                self.ui.label2.setText(
                    "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                self.table.points[0]))
                self.ui.label2.show()

    def processInputFile1 (self):
        if any(self.T):  # t < 15:  # 15 est arbitraire et modulable
            #print ("coucou")
            for i in range(self.table.plat.n):
                Plateau.proche_bord(self.table.plat, self.posx, self.posy, i)  # on gère les rebonds sur les bords

            Plateau.collisions(self.table.plat)  # on gère les collisions entre boules
            self.t += self.table.dt
            for i in range(self.table.plat.n):  # while self.T != np.array ([0 for i in range self.n]):
                self.T[i] = Boule.evolution(self.table.plat[i], self.table.dt, self.table.plat.k,
                                   0.05 * self.table.plat.be)  # détermination de la trajectoire de chaque boule, à l'instant t+1
                self.posx[i].append(self.table.plat[i].x)
                self.posy[i].append(self.table.plat[i].y)

            #print ("ça doit update")
            #self.drawEcosysteme1()
            self.ui.con.update()
            #print ("alors ?")
        else :
            self.timer.stop()
            self.ui.con.update()
            print ("billes immmmmmobiles")
            for i in range(self.table.plat.n):
                self.table.plat[i].vx, self.table.plat[i].vy = 0, 0

            if self.TEST[0] - self.table.plat[self.i % 2 - 1].x != 0 and self.TEST[1] - self.table.plat[self.i % 2 - 1].y  !=0 and self.TEST[2] - \
                self.table.plat[self.i % 2 - 2].x != 0 and self.TEST[3] - self.table.plat[self.i % 2 - 2].y != 0:
                print("Vous avez marqué un point")
                self.ui.label.setText("Vous avez marqué un point ! C'est encore à vous de jouer")
                self.ui.label.show()
                self.table.points[self.i % 2] += 1
                self.ui.label2.setText(
                    "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                self.table.points[0]))
                self.ui.label2.show()

            else:
                print("Pas de chance... Au joueur suivant")
                self.i += 1
                self.ui.label.setText(("Pas de chance... C'est à {} de jouer.").format(self.joueurs[self.i % 2]))
                self.ui.label.show()
                self.ui.label2.setText(
                    "{} : {} \n{} : {} ".format(self.joueurs[1], self.table.points[1], self.joueurs[0],
                                                self.table.points[0]))
                self.ui.label2.show()
            self.table.plat.queue.x , self.table.plat.queue.y = self.table.plat[self.i % 2].x+ 86.2, self.table.plat[self.i % 2].y + 86.2
            self.table.plat.queue.p = 0
            self.xp , self.yp =  self.table.plat.queue.x , self.table.plat.queue.y
            self.ui.con.update()


    def drawEcosysteme1(self,*args):
        qp = self.painter
        qp.begin(self.ui.con)
        self.painter2.begin (self.ui.con)

        for boullle in self.table.plat:
             #ins.dessin(qp)
             boullle.dessinimage(qp)
             #QtGui.QPainter().drawImage(QtCore.QRect(10 + 40 + boullle.x, 701 - boullle.y + 10 + 76.2, 20, 20), QtGui.QImage("blanche.jpg"))
             #print (self.egfw+self.bande_o+ boullle.x , boullle.y + self.ehfw + self.bande_s)    #10+ 76.2 + (51.3 + 90)+ (621 - ins.y))
        #print ("tructruc")

        if self.table.plat.queue.p == 0 :
            print ("on est laaaaaaaaaaaaaaaaaaaaaaa", self.table.plat.queue.p)
            #self.table.plat.queue.dessinimage (qp)
            boulex, bouley = self.table.plat[self.i % 2].x + 90, self.table.plat[self.i % 2].y + 88.2
            #boulex, bouley = self.table.plat[self.i % 2].x, self.table.plat[self.i % 2].y
            #dx, dy = self.table.plat.queue.x -6 - boulex, self.table.plat.queue.y-38 - bouley
            #dx, dy = self.table.plat.queue.x - boulex, self.table.plat.queue.y - bouley
            dx, dy = self.table.plat.queue.x - self.xp, self.table.plat.queue.y - self.yp
            if dx == 0:
                if dy < 0:
                    angle_b1 = -np.pi / 2
                else:
                    angle_b1 = np.pi / 2
            elif dy == 0:
                if dx > 0 :
                    angle_b1 = 0  #############
                else :
                    angle_b1 = -np.pi
            else:
                if dy > 0 and dx > 0:
                    angle_b1 = np.arctan(dy / dx)  # angle_b1 direction de la boule mobile
                elif dy < 0 and dx > 0:
                    angle_b1 = (- np.arctan(abs(dy / dx))) % (2 * np.pi)
                elif dy > 0 and dx < 0:
                    angle_b1 = np.pi - np.arctan(abs(dy / dx))
                else:
                    angle_b1 = np.pi + np.arctan(abs(dy / dx))

            #self.table.plat[self.i % 2].x = self.table.plat[self.i % 2].x + dx
            #self.table.plat[self.i % 2].y = self.table.plat[self.i % 2].y + dy

            self.table.plat.queue.alpha =angle_b1 % (2*np.pi) # + np.pi) % 2*np.pi
            angle = (self.table.plat.queue.alpha)*(180/np.pi)
            print ("angleeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",angle)

            if dx > 0 :
                distx = min (dx,300)
            else :
                distx = max(dx, -300)

            if dy > 0 :
                disty = min (dy,300)
            else :
                disty = max(dy, -300)

            if self.xp != self.table.plat.queue.x and self.xp != self.table.plat[self.i % 2].x + 86.2 :
                self.table.plat.point_clique.dessinimage(self.painter2, self.xp,
                                              self.yp)
            self.table.plat.queue.dessinimage(self.painter2 ,angle , boulex + distx ,bouley + disty)

        self.table.plat.point.dessinimage(self.painter, self.table.plat[self.i % 2].x,
                                              self.table.plat[self.i % 2].y)
        self.painter2.end()
        qp.end()


    def mousePressEvent (self,event):
        self.xp = event.x()
        self.yp = event.y()  #coordonnees du point de debut de cliquage (press)
        self.painter2.begin (self.ui.con)
        self.table.plat.point_clique.dessinimage(self.painter2, self.xp,
                                          self.yp)
        self.painter2.end()
        print (event.pos(), event.x(), event.y(), "laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" )

    def mouseMoveEvent (self,event): #affichage en direct des coordonnées (aide pour les tests)
        self.table.plat.queue.x = event.x()
        self.table.plat.queue.y = event.y()
        self.ui.con.update ()

        qp2 = self.painter2
        qp2.begin(self.ui.con)
        qp2.setBrush(Qt.black)
        qp2.drawLine(200, 200, 400, 400)

        qp2.drawLine(event.x(), event.y(), self.xp, self.yp)
        #self.painter.setPen(QtCore.Qt.red)
        qp2.drawLine(25, 25, 100, 100)
        #self.table.plat.queue.dessinimage (qp2, 10)
        qp2.end()
        #print (event.pos(), event.x(), event.y(), "looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo" )

    def mouseReleaseEvent (self,event):
        self.xr = event.x()
        self.yr = event.y() #coordonnees du point de fin de cliquage (release)

        dx, dy = self.xr - self.xp, self.yr - self.yp
        #dx, dy = self.xr - self.table.plat[self.i % 2].x , self.yr - self.table.plat[self.i % 2].y


        if dx == 0:
            if dy < 0:
                angle_b1 = -np.pi / 2
            else:
                angle_b1 = np.pi / 2
        elif dy == 0:
            if dx > 0:
                angle_b1 = 0  #############
            else:
                angle_b1 = -np.pi
        else:
            if dy > 0 and dx > 0:
                angle_b1 = np.pi+  np.arctan(dy / dx)  # angle_b1 direction de la boule mobile
            elif dy < 0 and dx > 0:
                angle_b1 = ( np.pi -np.arctan(abs(dy / dx))) % (2 * np.pi)
            elif dy > 0 and dx < 0:
                angle_b1 = - np.arctan(abs(dy / dx))
            else:
                angle_b1 =  np.arctan(abs(dy / dx))

        self.table.plat.queue.alpha2 = angle_b1*180/np.pi
        self.table.plat.queue.p = min ((dx**2 + dy**2) * 0.3, 1400)
        print ("iciciciciccici", self.table.plat.queue.p)
        #print (event.pos(), event.x(), event.y(), "lppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp" )

# class MaFenetre(QtWidgets.QMainWindow):
#      def __init__(self, parent=None):
#          super().__init__(parent)
#          zoneCentrale = QWidget()
#          prenom1 = QLineEdit(self)
#          prenom2 = QLineEdit(self)
#          layout = QFormLayout()
#          layout.addRow("prénom du joueur 1 ", prenom1)
#          layout.addRow("Prénom du joueur 2", prenom2)
#          zoneCentrale.setLayout(layout)
#          self.setCentralWidget(zoneCentrale)

         # QtWidgets.QMainWindow.resize(1123, 835)
         #
         # self.centralwidget = QtWidgets.QWidget(QtWidgets.QMainWindow)
         # self.centralwidget.resize (1123,835)
         # self.centralwidget.setObjectName("centralwidget")
         # self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)

         # self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
         # self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
         # self.horizontalLayout_2.setObjectName("horizontalLayout_2")
         # self.Plateau = QtWidgets.QWidget(self.horizontalLayoutWidget)
         # self.Plateau.setObjectName("Plateau")
         # self.horizontalLayout_2.addWidget(self.Plateau)

         #self.retranslateUi(QtWidgets.QMainWindow)
        #


     # def retranslateUi(self, mainWindow):
     #     _translate = QtCore.QCoreApplication.translate
     #     #mainWindow.setWindowTitle(_translate("mainWindow", "Entrez vos prénoms"))
     #     self.Bouton_Demarrer.setText(_translate("mainWindow", "Entrer"))

# class Ui_mainWindow2(QtWidgets.QMainWindow):
#     def setupUi2(self, mainWindow):
#         mainWindow.setObjectName("mainWindow")
#         mainWindow.setWindowModality(QtCore.Qt.NonModal)
#         mainWindow.resize(500, 300)
#         icon = QtGui.QIcon()
#         icon.addPixmap(QtGui.QPixmap("C:\\WPy64-3760\\python-3.7.6.amd64\\../../OneDrive - Ecole Nationale Supérieure de Techniques Avancées Bretagne/UE 2.4-projet/Sujet 05 - Billard/tablelogo.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
#         mainWindow.setWindowIcon(icon)
#
#         #zoneCentrale = QWidget ()
#
#          #nom = QLineEdit(self.ui)
#         #prenom = QLineEdit(self.ui)
#         #age = QLineEdit(self.ui)
#
#         #layout = QFormLayout()
#         #layout.addRow("Votre nom", nom)
#         #layout.addRow("Votre prénom", prenom)
#         #layout.addRow("Votre âge", age)
#         #zoneCentrale.setLayout(layout)
#         #self.setCentralWidget(zoneCentrale)
#
#
#
#         mainWindow.setDockNestingEnabled(False)
#         self.centralwidget = QtWidgets.QWidget(mainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
#         self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 180, 450, 45))
#         self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
#         self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#         self.Plateau = QtWidgets.QWidget(self.horizontalLayoutWidget)
#         self.Plateau.setObjectName("Plateau")
#         self.horizontalLayout_2.addWidget(self.Plateau)
#         self.Bouton_Demarrer = QtWidgets.QPushButton(self.horizontalLayoutWidget)
#         self.Bouton_Demarrer.setObjectName("Bouton_Demarrer")
#         self.horizontalLayout_2.addWidget(self.Bouton_Demarrer)
#         spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.horizontalLayout_2.addItem(spacerItem)
#         self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
#         self.label.setObjectName("label")
#         self.horizontalLayout_2.addWidget(self.label)
#         #spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         #self.horizontalLayout_2.addItem(spacerItem1)
#         self.Bouton_Quitter = QtWidgets.QPushButton(self.horizontalLayoutWidget)
#         self.Bouton_Quitter.setObjectName("Bouton_Quitter")
#         self.horizontalLayout_2.addWidget(self.Bouton_Quitter)
#
#         self.con = QtWidgets.QWidget(self.centralwidget)
#         self.con.setGeometry(QtCore.QRect(20, 20, 300, 251))
#         self.con.setObjectName("con")
#
#         mainWindow.setCentralWidget(self.centralwidget)
#
#         self.prenom1 = QLineEdit(self)
#         self.prenom2 = QLineEdit(self)
#         self.layout = QFormLayout()
#         self.layout.addRow("prénom du joueur 1 ", self.prenom1)
#         self.layout.addRow("Prénom du joueur 2", self.prenom2)
#         self.con.setLayout(self.layout)
#         self.setCentralWidget(self.con)
#
#
#         self.menubar = QtWidgets.QMenuBar(mainWindow)
#         self.menubar.setGeometry(QtCore.QRect(0, 0, 1123, 26))
#         self.menubar.setObjectName("menubar")
#         self.menuMenu = QtWidgets.QMenu(self.menubar)
#         self.menuMenu.setObjectName("menuMenu")
#         mainWindow.setMenuBar(self.menubar)
#
#
#         self.statusbar = QtWidgets.QStatusBar(mainWindow)
#         self.statusbar.setObjectName("statusbar")
#         mainWindow.setStatusBar(self.statusbar)
#
#
#         self.actionQuitter = QtWidgets.QAction(mainWindow)
#         self.actionQuitter.setObjectName("Entrer")
#         self.menuMenu.addAction(self.actionQuitter)
#         self.menubar.addAction(self.menuMenu.menuAction())
#
#         self.retranslateUi2(mainWindow)
#
#         self.Bouton_Quitter.clicked.connect(self.suite)
#         #self.actionQuitter.triggered.connect(mainWindow.close)
#
#         QtCore.QMetaObject.connectSlotsByName(mainWindow)
#
#     def suite (self):
#         window = MonAppli()
#         window.show()
#         self.close()
#
#     def retranslateUi2(self, mainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         mainWindow.setWindowTitle(_translate("mainWindow", "Table de billard"))
#         self.Bouton_Demarrer.setText(_translate("mainWindow", "Démarrer"))
#         self.label.setText(_translate("mainWindow", "     A vous de jouer  !             "))
#         self.Bouton_Quitter.setText(_translate("mainWindow","Entrer"))
#         self.menuMenu.setTitle(_translate("mainWindow", "Menu"))
#         self.actionQuitter.setText(_translate("mainWindow", "Quitter"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    #fen = MaFenetre ()
    #t = Ui_mainWindow2()
    #t.show()
    window.show()
    #fen.show()
    app.exec_()

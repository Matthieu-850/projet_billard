import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic #QPixmap
#from QPixmap import QMatrix
from interfaceBon import Ui_mainWindow
from projet_8_GitHub import Partie, Boule_blanche, Boule, Plateau
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget #QPixmap
import numpy as np
#from QtGui import QMatrix
#from PySide2 import QtGui
import time


# l'approche par héritage simple de la classe QMainWindow (même type de notre fenêtre
# créée avec QT Designer. Nous configurons après l'interface utilisateur
# dans le constructeur (la méthode init()) de notre classe

class MonAppli(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        #y = self.ui.con.height()
        #x = self.ui.con.width()
        pixmap = QtGui.QPixmap("carambole_mouche3.jpg")
        #pixmap.resize (x,y)
        #QtGui.QPixmap.scaled(pixmap, x, y)
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

        self.painter = QtGui.QPainter()
        self.painter2 = QtGui.QPainter()
        #self.ui.con.update = self.drawEcosysteme1
        self.ui.con.paintEvent = self.drawEcosysteme1

        self.hw =  self.ui.con.height()   ###701  # (y) hauteur du widget con, ie la table
        self.lw =  self.ui.con.width()   #1101# (x) largeur du widget
        #self.hw = 621
        #self.lw = 971
        print("selon les x",self.lw, "  selon les y", self.hw)
        self.bande_n, self.bande_o, self.bande_e, self.bande_s = 76.2, 76.2, 76.2, 51.3  # epaisseurs des bandes sur notre image de table
        self.ehfw, self.egfw = 10, 10  # ecart haut fenetre - widget, ecart gauche fenetre - widget
        self.by, self.bx = self.hw - self.bande_n - self.bande_s, self.lw - self.bande_e - self.bande_o  # taille du tapis, correspondent à self.bn et self.be dans la classe plateau
        self.xp,self.yp, self.xr,self.yr = 0,0,0,0


        self.table = Partie(10, 0.005, self.bx, self.by)
        for bal in self.table.plat :
            print (bal.r)

        # self.ui.bouton_pas.clicked.connect(self.un_pas)
        self.ui.Bouton_Demarrer.clicked.connect(self.demarrer)
        self.ui.Bouton_Jouer.clicked.connect(self.jouer)

        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.ui.con.update())

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.processInputFile1)

        #self.timer.start(200)
        #self.demarrer()

        qp = self.painter
        #self.painter2.begin(self.ui.con)
        #self.table.plat.queue.dessinimage(self.painter2,self.table.plat.queue.alpha)
        #self.painter2.end()

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
            print ("billes immmmmmobiles")
            for i in range(self.table.plat.n):
                self.table.plat[i].vx, self.table.plat[i].vy = 0, 0

            if self.TEST[0] - self.table.plat[self.i % 2 - 1].x != 0 and self.TEST[1] - self.table.plat[self.i % 2 - 1].y  !=0 and self.TEST[2] - \
                self.table.plat[self.i % 2 - 2].x != 0 and self.TEST[3] - self.table.plat[self.i % 2 - 2].y != 0:
                print("Vous avez marqué un point")
                self.table.points[self.i % 2] += 1

            else:
                print("Pas de chance... Au joueur suivant")
                self.i += 1

    def processInputFile (self):
        if self.table. c < self.table.nb_coups :
            self.table.c += 1
            self.table.plat.un_coup (self.table.dt, self.table.c )
            # self.ui.con.update ()
        else :
            self.ui.con.update ()
            self.timer.stop()
            print("Fini")

        #QtCore.connect(self.timer, QtCore.QTimer.timeout, self, self.ui.con.update())
        #self.timer.start()


        #self.ui.con.update()
    #def un_pas(self):
    #    #        print("un pas")
    #    #        self.ecosys.unTour()
    #    #        self.ui.centralwidget.update()
    #    if self.table.nb_coups > 0:
    #        print("gogogo")
    #        self.table.plat.un_coup()
    #        self.table.plat.nb_coups-= -1
    #        self.ui.con.update()  # nécessaire pour la MAJ de l’IHM
    #    else:
    #        self.timer.stop()
    #        print("Fini")

    def demarrer(self):
        print("Demarrer")
        # Q7 -----------------------------------------------

        self.table = Partie(3, 0.02,self.lw ,self.hw)  #self.ui.con.width(), self.ui.con.height()) # 971-20*2-80 # 621-40*2
        print( "partie crée")
        #self.timer.start (200)
        self.ui.con.update()

    def jouer1(self):
        # self.timer.start(20000)
        print("Jouer")
        if self.table.c < self.table.nb_coups:
            self.table.c += 1
            self.table.plat.un_coup(self.table.dt, self.table.c)
            # self.ui.con.update ()
        else:
            #self.ui.con.update()
            self.timer.stop()
            print("Fini")
        #self.table.jouer()
        #self.ui.centralwidget.update()

    def jouer (self):  #un coup
        print ("tour {}".format (self.table.c))
        if self.table.c < self.table.nb_coups :
            self.table.c+=1
            x1, y1, x2, y2 = self.table.plat[self.i%2 -1].x, self.table.plat[self.i%2 -1].y, self.table.plat[self.i%2 -2].x, self.table.plat[self.i%2 -2].y
            self.TEST = [x1, y1, x2, y2] #liste contenant les positions de boules non tapees juste avant le coup

            #self.table.plat.un_coup (self.plat, self.dt, self.c,i %2)
            print("c'est au joueur {} de jouer".format(self.i%2))
            self.T = np.array([1 for i in range(self.table.plat.n)])
            #Boule_blanche.impulsion(self.table.plat[self.i%2], int(input("cap")), float(input("Vitesse")))  # 1 boule blanche

            #while self.table.plat.queue.p == 0 :
            #    pass

            #Boule_blanche.impulsion(self.table.plat[self.i % 2], 35, 400)  # 1 boule blanche
            Boule_blanche.impulsion(self.table.plat[self.i % 2], self.table.plat.queue.alpha, self.table.plat.queue.p)
            self.table.plat.queue.p = 0
            self.t = 0
            self.posx, self.posy = [[] for i in range(self.table.plat.n)], [[] for i in
                                                       range(self.table.plat.n)]  # pour garder en mémoire les positions passées
            for i in range(self.table.plat.n):
                self.posx[i].append(self.table.plat[i].x)
                self.posy[i].append(self.table.plat[i].y)
            # plt.ion()       , et surtout la précédente
            # for i in range (self.n):
            # plt.scatter(posx[i][0], posy[i][0], s=90, color='k')  # point de départ de chaque boule, en noir
            # plt.scatter(posx[joueur][0], posy[joueur][0], s=90, color='y')  # point de départ de chaque boule, en noir
            self.timer.start (7)

        else :
            print ("Joueur 1 : {} points /n Joueur 2 : {} points ".format (self.table.points[1], self.table.points[0]))
            if self.table.points[0] != self.table.points[1]:
                if self.table.points [0] > self.table.points [1]:
                    g = '2'
                else:
                    g = '1'
                print ("Le joueur {} a gagné ! Félicitations !".format (g))
            else :
                print ("Egalité ! Bravo à vous deux !")

    #def paintEvent(self, e):
    #    qp = QtGui.QPainter()
    #    qp.begin(self)
    #    self.drawEcosysteme1(qp)
    #    qp.end()


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

            #self.table.plat.queue.dessinimage (qp)
            boulex, bouley = self.table.plat[self.i % 2].x + 90, self.table.plat[self.i % 2].y + 88.2
            dx, dy = self.table.plat.queue.x -6 - boulex, self.table.plat.queue.y-38 - bouley
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
            #self.table.plat.queue.alpha =(angle_b1 + np.pi) % 2*np.pi
            #Image = QtGui.QImage("queue_billard2.png").transformed(PySide2.QtGui.QMatrix().rotate(angle_b1))
            #Image = QtGui.QImage("queue_billard2.png").\
            #self.painter.rotate(0)
            angle = ((self.table.plat.queue.alpha)*180/np.pi)%(2*np.pi)
            #self.painter2.rotate(angle)
            #self.painter2.translate(self.rect().bottomRight())
            #self.painter2.rotate(-63)
            #PySide2.QtGui.QMatrix.rotate(angle_b1)
            self.table.plat.queue.dessinimage(self.painter2 ,angle , boulex,bouley)
            #self.painter2.rotate(0)
        self.painter2.end()
        qp.end()

    def drawEcosysteme(self,*args):
            #        qp.setPen(QtCore.Qt.red)
        for ins in self.table.plat:
      #      # qp.drawEllipse(ins.x,ins.y, 10,5)
            if ins.color == 'yellow':
                self.painter.setPen(QtCore.Qt.yellow)
                self.painter.drawRect(ins.x, ins.y, 10, 5)
            else:
                self.painter.setPen(QtCore.Qt.red)
                self.painter.drawEllipse(ins.x, ins.y, 10, 5)

    def mousePressEvent (self,event):
        self.xp = event.x()
        self.yp = event.y()  #coordonnees du point de debut de cliquage (press)
        print (event.pos(), event.x(), event.y(), "laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" )

    def mouseMoveEvent (self,event): #affichage en direct des coordonnées (aide pour les tests)
        self.table.plat.queue.x = event.x()
        self.table.plat.queue.y = event.y()
        self.ui.con.update ()
        #qp = self.painter
        #qp.begin(self.ui.con)
        #self.table.plat.queue.dessinimage (qp)
        #qp.end()
        print (event.pos(), event.x(), event.y(), "looooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo" )

    def mouseReleaseEvent (self,event):
        self.xr = event.x()
        self.yr = event.y() #coordonnees du point de fin de cliquage (release)

        dx, dy = self.xr - self.xp, self.yr - self.yp

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



           # elif dy < 0 and dx > 0 :
           #     angle_b1 = (np.pi + np.arctan(abs (dy / dx)))
           # elif dy > 0 and dx < 0 :
           #     angle_b1 = np.arctan(-dy / dx)


        self.table.plat.queue.alpha = angle_b1*180/np.pi
        self.table.plat.queue.p = (dx**2 + dy**2) * 0.1
        print (event.pos(), event.x(), event.y(), "lppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp" )


class Queue (QWidget) :
    def __init__(self):
        super().__init__ ()
        self.x = 0
        self.y = 0
        self.al = 0
        self.p = 0

    def mousePressEvent (self,event):
        self.x = event.x()
        self.y = event.y()
        print (event.pos(), event.x(), event.y(), "laaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa" )





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    window.show()
    app.exec_()

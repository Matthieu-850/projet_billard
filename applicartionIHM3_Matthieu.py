import sys
from PyQt5 import QtGui, QtCore, QtWidgets, uic
from interface5 import Ui_mainWindow
from projet_7 import Partie
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

        pal = QtGui.QPalette()
        pal.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
        self.ui.con.lower()
        self.ui.con.stackUnder(self)
        self.ui.con.setAutoFillBackground(True)
        self.ui.con.setPalette(pal)

        self.painter = QtGui.QPainter()
        self.ui.con.paintEvent = self.drawEcosysteme1


        self.hw =  self.ui.con.height()   ###701  # (y) hauteur du widget con, ie la table
        self.lw =  self.ui.con.width()   #1101# (x) largeur du widget
        print(self.hw, self.lw)
        self.bande_n, self.bande_o, self.bande_e, self.bande_s = 76.2, 76.2, 76.2, 51.3  # epaisseurs des bandes sur notre image de table
        self.ehfw, self.egfw = 10, 10  # ecart haut fenetre - widget, ecart gauche fenetre - widget
        self.by, self.bx = self.hw - self.bande_n - self.bande_s, self.lw - self.bande_e - self.bande_o  # taille du tapis, correspondent à self.bn et self.be dans la classe plateau


        self.table = Partie(3, 0.1, self.lw, self.hw)

        # self.ui.bouton_pas.clicked.connect(self.un_pas)
        self.ui.Bouton_Demarrer.clicked.connect(self.demarrer)
        self.ui.Bouton_Jouer.clicked.connect(self.jouer)

        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.ui.con.update())

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.processInputFile1)
        #self.timer.start(200)
        #self.demarrer()

    def processInputFile1 (self):
        self.ui.con.update()

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

        self.table = Partie(3, 0.1,self.lw ,self.hw)  #self.ui.con.width(), self.ui.con.height()) # 971-20*2-80 # 621-40*2
        print( "partie crée")
        self.timer.start (200)
        #self.ui.con.update()

    def jouer(self):
        """on simule un coup de queue :
                on met en mouvement la/les boules blanches, et on traite collisions entre boules et avec la paroi.
                On trace, la trajectoire de chaque boule, ainsi que sa position de départ (en noir) et d'arrivée (en rouge)
                """
        print("c'est au joueur {} de jouer".format(self.table.plat.joueur))
        T = np.array([1 for i in range(self.table.plat.n)])
        table.plat.Boule_blanche.impulsion(self.table.plat[joueur], int(input("cap")), float(input("Vitesse")))  # 1 boule blanche
        t = 0

        posx, posy = [[] for i in range(self.n)], [[] for i in range(self.n)]  # pour garder en mémoire les positions passées
        for i in range(self.table.plat.n):
            posx[i].append(self.table.plat[i].x)
            posy[i].append(self.table.plat[i].y)
        self.ui.con.update()

        while any(T):  # t < 15:  # 15 est arbitraire et modulable
            for i in range(self.table.plat.n):
                self.table.plat.proche_bord(posx, posy, i)  # on gère les rebonds sur les bords
            self.table.plat.collisions()  # on gère les collisions entre boules
            t += dt
            for i in range(self.table.plat.n):  # while self.T != np.array ([0 for i in range self.n]):
                T[i] = table.plat.Boule.evolution(self.table.plat[i], dt, self.table.plat.k, 0.05 * self.table.plat.be)  # détermination de la trajectoire de chaque boule, à l'instant t+1
                posx[i].append(self.table.plat[i].x)
                posy[i].append(self.table.plat[i].y)
            self.ui.con.update()

        # if self.mode != 2:
        #    for i in range (self.n):
        #        self.proche_trou (self[i],i)
        # if len(posx[0]) > 1:

        for i in range(self.table.plat.n):
           self.table.plat[i].vx, self.table.plat[i].vy = 0, 0

        # self.timer.start(20000)
        print("Jouer")
        if self.table.c < self.table.nb_coups:
            self.table.c += 1
            self.table.plat.un_coup(self.table.dt, self.table.c)
            # self.ui.con.update ()
        else:
            self.ui.con.update()
            self.timer.stop()
            print("Fini")
        #self.table.jouer()
        #self.ui.centralwidget.update()


    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawEcosysteme(qp)
        qp.end()

        # --------------------------------------------

    def drawEcosysteme(self, qp):

            #        qp.setPen(QtCore.Qt.red)
        for ins in self.table.plat:
          # qp.drawEllipse(ins.x,ins.y, 10,5)r
            if ins.color == 'yellow':
                qp.setPen(QtCore.Qt.yellow)
                qp.drawRect(ins.x, ins.y, 10, 5)
            else:
                qp.setPen(QtCore.Qt.red)
                qp.drawEllipse(ins.x, ins.y, 10, 5)

    def drawEcosysteme1(self,qp):
        qp = self.painter
        qp.begin(self.ui.con)
        for boullle in self.table.plat:
             #ins.dessin(qp)
             boullle.dessinimage(qp)
             print (self.egfw+self.bande_o+ boullle.x , self.hw - boullle.y + self.ehfw + self.bande_n)    #10+ 76.2 + (51.3 + 90)+ (621 - ins.y))
        self.painter.end()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MonAppli()
    window.show()
    app.exec_()

import numpy as np
from numpy.random import randint
from matplotlib import pyplot as plt
import time
from PyQt5 import QtGui, QtCore
#from applicartionIHM3 import MonAppli
from abc import ABCMeta, abstractmethod


class Boule(metaclass = ABCMeta):  # une boule (blanche ou colorée), ses caractéristiques (physiques et cinétiques)
    def __init__(self, x, y, r=0.3, m=1):  # r le rayon, m la masse
        self.x = x
        self.y = y
        self.r = r
        self.m = m
        self.coord = np.array([self.x, self.y])
        self.vx = 0
        self.vy = 0
        self.vitesse = np.array([self.vx, self.vy])
        # self.ax, self.ay = 0,0

    @abstractmethod
    def dessinimage (self,qp) :
        pass


    def evolution(self, dt,k, eps = 0.5):  # on suppose le mouvement rectiligne uniforme,
        """
        on suppose le mouvement des boules rectiligne uniforme, en l'absence de collisions (bords ou autres boules).
        La position est fonction affine du temps
        entrée : float
        sortie : array -> nouvelles coordonnées de la boule
        """
        if self.vx**2 + self.vy**2 < eps :
            self.vx = 0
            self.vy = 0
            return 0
        else :
            self.vx = k*self.vx
            self.vy = k * self.vy
            self.x += dt * self.vx
            self.y += dt * self.vy
            return 1

    def rebond(self, bord):
        """
        simule un rebond sur une paroi droite
        entrée : string caractérisant la paroi sur laquelle il y a rebonb
        sortie : la nouvelle vitesse de la boule, après rebond
        """
        if bord in ['N', 'S']:
            self.vy = - self.vy
        elif bord in ['O', 'E']:
            self.vx = - self.vx
        return self.vitesse

    def tombe(self):
        self.x, self.y, self.vx, self.z = -0.5,-0.5,0,0
        self.color = 'k'

    def coll(self, boule2):
        alpha = np.linspace (0,360,100)
        alpha = np.pi * alpha /180
        d = abs ((self.x + self.r - boule2.x)**2 + boule2.y**2 )
        angle = 0
        for a in alpha :
            da = abs ((self.x + self.r*np.cos (a) - boule2.x)**2 + (self.y + self.r*np.sin (a)- boule2.y)**2 )
            if d > da :
                angle, d = a , da   # pour le point tangent au 2 boule, angle formé par Ox et la droite passant par le centre de la 1ere boule et le point tangent
        #angle_collision = (angle_b1 + angle)/2
        v1 = (self.vx**2 + self.vy**2)**0.5
        v2 = (boule2.vx ** 2 + boule2.vy ** 2) ** 0.5
        if v1 == 0 :
            if boule2.vx == 0:
                if boule2.vy < 0:
                    angle_b1 = -np.pi / 2
                else:
                    angle_b1 = np.pi / 2
            elif boule2.vy == 0:
                if boule2.vx > 0 :
                    angle_b1 = np.pi
                else :
                    angle_b1 = -np.pi
            else:
                if boule2.vy > 0 and boule2.vx > 0:
                    angle_b1 = np.arctan(boule2.vy / boule2.vx)  # angle_b1 direction de la boule mobile
                elif boule2.vy < 0 and boule2.vx > 0:
                    angle_b1 = (- np.arctan(abs(boule2.vy / boule2.vx))) % (2 * np.pi)
                elif boule2.vy > 0 and boule2.vx < 0:
                    angle_b1 = np.pi - np.arctan(abs(boule2.vy / boule2.vx))
                else:
                    angle_b1 = np.pi + np.arctan(abs(boule2.vy / boule2.vx))
            angle = (angle + np.pi )% (2*np.pi)
            d_angle = (abs(angle_b1 - angle))    #
            v1_p = v2*np.cos(d_angle)
            v2_p = v2*np.sin (d_angle)
            boule2.vx, boule2.vy, self.vx, self.vy = v2_p*np.cos ((2*angle_b1 - angle)%2*np.pi), v2_p*np.sin ((2*angle_b1- angle)%2*np.pi), v1_p*np.cos (angle ), v1_p*np.sin (angle)
        else :
            if self.vx == 0:
                if self.vy < 0:
                    angle_b1 = -np.pi / 2
                else:
                    angle_b1 = np.pi / 2
            elif self.vy == 0:
                if self.vx > 0 :
                    angle_b1 = np.pi
                else :
                    angle_b1 = -np.pi
            else:
                if self.vy > 0 and self.vx > 0 :
                    angle_b1 = np.arctan(self.vy / self.vx)
                elif self.vy<0 and self.vx > 0 :
                    angle_b1 = (- np.arctan(abs(self.vy / self.vx))) % 2 * np.pi
                elif self.vy > 0 and self.vx< 0 :
                    angle_b1 = np.pi - np.arctan(abs(self.vy / self.vx))
                else :
                    angle_b1 = np.pi + np.arctan(abs(self.vy / self.vx))
            d_angle = abs(angle_b1 - angle)  % (np.pi /2) #appatient à [0; pi/2]
            v1_p = v1*np.sin(d_angle)
            v2_p = v1*np.cos (d_angle)
            boule2.vx, boule2.vy, self.vx, self.vy = v2_p*np.cos (angle), v2_p*np.sin (angle), v1_p*np.cos ((2*angle_b1 - angle)%(2*np.pi)), v1_p*np.sin ((2*angle_b1  -angle)%(2*np.pi))
        print ("angle :", d_angle*180/np.pi, self.vx,self.vy,v1_p, v2_p)


class Boule_coloree(Boule):  # on définit la classe représentant les boules colorées, classe qui hérite de la classe boule
    image = QtGui.QImage("rouger.png")
    def __init__(self, x, y, r = 0.03):
        super().__init__(x, y,r)
        self.color = ['red', 'green', 'orange', 'blue'][randint(1, 4)]
    # une couleur au hasard pour chaque boule colorée

    # def dessin(self, qp):
    #     qp.setPen(QtCore.Qt.red)
    #     qp.drawEllipse(10+self.x,20+ 1000- self.y, 12, 7)

    def dessinimage(self, qp):
        #qp.drawImage(QtCore.QRect(self.x - 10, self.y - 10, 20, 20), self.image)
        qp.drawImage(QtCore.QRect(10+ self.x+50 , self.y + 10 + 52,35.5,35.5 ), self.image) #10+76.2+51.3+ 90 +621 - self.y,20,20), self.image)   #à tester

class Boule_blanche(Boule):  # on définit la classe représentant les boules colorées,
    image = QtGui.QImage("blancher.png")
    def __init__(self, x, y, r = 0.03):  #classe qui hérite de la classe boule
        super().__init__(x, y,r)
        self.color = 'yellow'  # les boules blanches sont représentées en jaune par soucis de lisibilité

    def impulsion(self, cap_V0, norme_V0):
        """Met en mouvement la boule blanche.
        Caractéristique propre aux boules blanches, elle sont propulsées par un coup de queue,
        représenté ici par une vitesse initiale non nulle v0
        entrée : array -> vitesse donnée à la boule blanche
        Modification effective de la vitesse de cette boule
        """
        self.vy = norme_V0 * np.sin(cap_V0 * np.pi / 180) #v0[0]
        self.vx = norme_V0 * np.cos(cap_V0 * np.pi / 180) #v0[1]

    def dessin(self, qp):
        qp.setPen(QtCore.Qt.red)
        qp.drawEllipse(10+self.x, 20+ self.bn- self.y, 12, 7)

    def dessinimage(self, qp):
        #qp.drawImage(QtCore.QRect(self.x - 10, self.y - 10, 20, 20), self.image)
        qp.drawImage(QtCore.QRect(10+self.x +50 ,self.y + 10 + 52,30,30), self.image)   #10+76.2 + 51.3 + 90+ 621- self.y, 20, 20), self.image)  #72.6, 76.2

class Plateau(list):  # le plateau est un espace délimité, composé d'une liste de boules
    def __init__(self, l=10, L=10, nb=1, nc=4, k = 0.998, mode = 0):
        super().__init__(self)
        self.bs, self.bn, self.bo, self.be = l, 0, 0, L
        self.nc, self.nb = nc, nb  # nombre de boules colorées, et blanches
        self.n = nb + nc  # nombre total de boules
        self.k = k
        self.mode = mode
        self.queue = Queue()
        self.point = Point()
        self.point_clique = Point_clique()
        #self.T = np.array ([1 for i in range (self.n)])

        if self.mode == 1 : #Le joueur choisit où placer chaque boule
            for i in range(nb):  # nomre de boules blanches sur le tapis
                print("placement d'une boule blanche")
                self.append(Boule_blanche(float(input("abscisse")), float(input("ordonnee"))))
            for i in range(nc):  # nombre de boules colorées sur le tapis
                print("placement d'une boule coloree")
                self.append(Boule_coloree(float(input("abscisse")), float(input("ordonnee"))))

        elif self.mode == 2 : # Mode billard français
            #self.append(Boule_blanche(0,0, r=4 * self.be * 0.03 / 2.54))
            #self.append(Boule_blanche(self.be, self.bs, r=self.be * 0.03 / 2.54))
            #self.append(Boule_blanche ( 100, 300, r=self.bo * 0.03 / 2.54))
            self.append(Boule_blanche(0.2 * self.be, 0.75 * self.bs, r= 1.3*self.be * 0.03 / 2.54))
            self.append(Boule_blanche(0.2 * self.be, 0.25 * self.bs, r=1.3*self.be * 0.03 / 2.54))
            self.append(Boule_coloree(0.8 * self.be, 0.5 * self.bs, r=1.3*self.be * 0.03 / 2.54))
            self.n = 3

        elif self.mode == 3: # Mode billard anglais
             pass

        elif self.mode == 0 : #Les boules sont toutes placées aléatoirement
            for i in range(nb):  # nomre de boules blanches sur le tapis
                self.append(Boule_blanche(randint(self.be), randint(self.bs)))
            for i in range(nc):  # nombre de boules colorées sur le tapis
                self.append(Boule_coloree(randint(self.be), randint(self.bs)))

    def proche_bord(self, posx, posy, i):
        """
         Si une boule est proche d'un bord, et qu'on constate que la boule se rapproche de ce bord,
        on appelle la fonction rebond, en précisant sur quel paroi il a lieu
        entrée : posx : liste des abscisses de chaque boule, posy : liste des ords de chaque boule, i : int
        """
        if self[i].x < 0.02*self.be:  # on est proche d'un bord
            if (len(posx[0]) <= 1) or (posx[i][-2] > self[i].x):  # on vérifie qu'on est pas en tout début de simulation,
                Boule.rebond(self[i], 'O')  # ou que l'on est pas déjà en train de repartir du bord
        elif self[i].x > self.be *(1- 0.02):
            if len(posx[0]) <= 1 or posx[i][-2] < self[i].x:
                Boule.rebond(self[i], 'E')
        elif self[i].y < 0.02*self.bs:
            if len(posx[0]) <= 1 or posy[i][-2] > self[i].y:
                Boule.rebond(self[i], 'N')
        elif self[i].y > self.bs * (1- 0.02):
            if len(posx[0]) <= 1 or posy[i][-2] < self[i].y:
                Boule.rebond(self[i], 'S')

    def collisions(self):
        """"
        Détection de chaque collision imminente entre les boules, et simulation de la déviation de trajectoire associée
        On mesure la distance entre chaque centre de boule. Si elle est trop proche, il y a collision : échange de quantité de mvt
        """
        col = []
        for i in range(len(self)-1):
            for j in range(i + 1, len(self)):  # on teste la collision de chaque couple de boules une fois
                if ((self[i].x - self[j].x) ** 2 + (self[i].y - self[j].y) ** 2) ** 0.5 <= self[i].r*(1+0.002) + self[j].r:
                    col.append([i, j])  # boules trop proches, leur trajectoire va être déviée par la collision
        for [i, j] in col:
            Boule.coll (self[i],self[j])
            #self[i].vx, self[i].vy, self[j].vx, self[j].vy = self[j].vx + (self[j].vy)/3, self[j].vy, self[i].vx + (self[i].vy)/3, self[i].vy
            # les boules échangent leur quantité de mouvement quand elles entrent en collision (toutes de masse identiques ici)
        #print ("colllllllllllllllllllllllllllllllllllllllllllllllllll", col)

    def un_coup(self, dt,c,joueur=1):
        """on simule un coup de queue :
        on met en mouvement la/les boules blanches, et on traite collisions entre boules et avec la paroi.
        On trace, la trajectoire de chaque boule, ainsi que sa position de départ (en noir) et d'arrivée (en rouge)
        """
        print ("c'est au joueur {} de jouer".format (joueur))
        T = np.array ([1 for i in range (self.n)])
        Boule_blanche.impulsion(self[joueur], 48, 400)  # 1 boule blanche
        #Boule_blanche.impulsion(self[joueur], int(input("cap")), float(input("Vitesse")))  # 1 boule blanche
        t = 0
        #plt.figure(1)
        #plt.xlim((-0.5, self.bord_est+ 0.5))
        #plt.ylim((-0.5, self.bord_nord + .5))
        posx, posy = [[] for i in range(self.n)], [[] for i in
                                                   range(self.n)]  # pour garder en mémoire les positions passées
        for i in range(self.n):
            posx[i].append(self[i].x)
            posy[i].append(self[i].y)
        # plt.ion()       , et surtout la précédente
        #for i in range (self.n):
            #plt.scatter(posx[i][0], posy[i][0], s=90, color='k')  # point de départ de chaque boule, en noir
        #plt.scatter(posx[joueur][0], posy[joueur][0], s=90, color='y')  # point de départ de chaque boule, en noir
        while any (T):     # t < 15:  # 15 est arbitraire et modulable
            for i in range(self.n):
                self.proche_bord(posx, posy, i)  # on gère les rebonds sur les bords
            self.collisions()  # on gère les collisions entre boules
            t += dt
            for i in range(self.n): # while self.T != np.array ([0 for i in range self.n]):
                T[i] = Boule.evolution(self[i], dt,self.k, 0.05*self.be)  # détermination de la trajectoire de chaque boule, à l'instant t+1
                posx[i].append(self[i].x)
                posy[i].append(self[i].y)
            #MA = MonAppli ()
           # MA.ui.con.update()
            #if self.mode != 2:
            #    for i in range (self.n):
            #        self.proche_trou (self[i],i)
            #if len(posx[0]) > 1:
                #for i in range(self.n):
                    #plt.plot([posx[i][-2], posx[i][-1]], [posy[i][-2], posy[i][-1]], color=self[i].color)
                    #plt.title('trajectoire des boules, coup {}'.format(c))
            #time.sleep(1) #demander à Théo
        for i in range(self.n):
            #plt.scatter(posx[i], posy[i], s=60,
                      #  color=self[i].color)  # ensemble des positions de chaque boule, à chaque instant t (pas de dt)
            #plt.scatter(posx[i][-1], posy[i][-1], s=60, color='r')  # point d'arrivée de chaque boule, en rouge
            self[i].vx, self[i].vy = 0,0
        #plt.show()

class Partie ():
    def __init__ (self, nb_coups, dt, LL = 10, ll=10):
        self.nb_coups = nb_coups
        self.dt = dt
        self.c = 0  # on s'arrête à nb_coups
        #self.plato = plat
        self.points = [0,0]  #en position 0, le joueur 2
        self.l = ll
        self.L= LL
        self.plat = Plateau(mode=2, l=self.l, L=self.L)

    def jouer (self) :
        i = 1
        while self.c < self.nb_coups :
            #plt.figure ()
            self.c+=1
            TEST = [self.plat[i%2 -1].vx,self.plat[i%2 -1].vy, self.plat[i%2 -2].vx, self.plat[i%2 -2].vy]
            Plateau.un_coup (self.plat, self.dt, self.c,i %2)
            if TEST[0] - self.plat[i%2 -1].vx == 0 and TEST [1] - self.plat[i%2 -1].vy and TEST[2] - self.plat[i%2 -2].vx == 0 and TEST [3] - self.plat[i%2 -3].vy ==0 :
                print ("Vous avez marqué un point")
                self.points [i %2] += 1
            else :
                print ("Pas de chance... Au joueur suivant")
                i += 1
        print ("Joueur 1 : {} points /n Joueur 2 : {} points ".format (self.points[1], self.points[0]))
        if self.points[0] != self.points[1]:
            if self.points [0] > self.points [1]:
                g = 2
            elif self.points [0] > self.points [1]:
                g = 1
            print ("Le joueur {} a gagné ! Félicitations !".format (g))
        else :
            print ("Egalité ! Bravo à vous deux !")

class Queue ():
    LISTE =["qb24-removebg-preview.png", "qb1-removebg-preview.png", "qb2-removebg-preview.png", "qb3-removebg-preview.png", "qb4-removebg-preview.png", "qb5-removebg-preview.png", "qb6-removebg-preview.png", "qb7-removebg-preview.png", "qb8-removebg-preview.png", "qb9-removebg-preview.png","qb10-removebg-preview.png", "qb11-removebg-preview.png", "qb12-removebg-preview.png", "qb13-removebg-preview.png", "qb14-removebg-preview.png", "qb15-removebg-preview.png", "qb16-removebg-preview.png", "qb17-removebg-preview.png", "qb18-removebg-preview.png", "qb18-removebg-preview.png", "qb19-removebg-preview.png", "qb20-removebg-preview.png", "qb21-removebg-preview.png", "qb22-removebg-preview.png", "qb23-removebg-preview.png"]
    l = QtGui.QImage("qb8-removebg-preview.png")
    def __init__(self):
        #self.l = QtGui.QImage ("qb8-removebg-preview.png")
        self.x = 900
        self.y = 120
        self.p = 0
        self.alpha = 50
        self.alpha2 = 0

    def dessinimage(self, qp,angle, boulex=-10,bouley=-10):
        LISTE = ["qb24-removebg-preview.png", "qb1-removebg-preview.png", "qb2-removebg-preview.png",
                 "qb3-removebg-preview.png", "qb4-removebg-preview.png", "qb5-removebg-preview.png",
                 "qb6_90-removebg-preview.png", "qb7-removebg-preview.png", "qb8-removebg-preview.png",
                 "qb9-removebg-preview.png", "qb10_180-removebg-preview.png", "qb11-removebg-preview.png",
                 "qb12_180-removebg-preview.png", "qb13-removebg-preview.png", "qb14-removebg-preview.png",
                 "qb15-removebg-preview.png", "qb16-removebg-preview.png", "qb17-removebg-preview.png",
                 "qb18-removebg-preview.png", "qb18-removebg-preview.png", "qb19-removebg-preview.png",
                 "qb20-removebg-preview.png", "qb21-removebg-preview.png", "qb22-removebg-preview.png",
                 "qb23-removebg-preview.png"]
        self.l = QtGui.QImage (LISTE[int(angle * 24 / 360)])
        #print (self.l)
        #print (LISTE)
        #if boulex == -10 :
            #qp.drawImage(QtCore.QRect(self.x-6, self.y - 38 ,300, 15), self.image)
            #print(self.x, self.y)
        #qp.drawImage(QtCore.QRect(self.x - 10, self.y - 10, 20, 20), self.image)
        #qp.drawImage(QtCore.QRect(self.x -150*(np.cos(self.alpha)),self.y-35*(np.sin(self.alpha)),300,15), self.image )   #10+76.2 + 51.3 + 90+ 621- self.y, 20, 20), self.image)
#        qp.translate(self.image.bottomRight())
        #else :
            #qp.rotate(angle)
        qp.drawImage(QtCore.QRect(boulex-290 -21.5, bouley-285 -24.2, 600, 600) ,self.l)
        #qp.drawImage(QtCore.QRect(17,40, 300, 15), self.image)
        #print(boulex, bouley - 35)
        #print ("yep")

class Point ():
    image = QtGui.QImage("point2.png")

    def dessinimage(self, qp, boulex,bouley):
        qp.drawImage(QtCore.QRect(boulex +93 -23 , bouley+95 -24.6, 10, 10), self.image)
        #print (boulex + 86.2, bouley + 86.20)

class Point_clique ():
    image = QtGui.QImage("point_clique.png")

    def dessinimage(self, qp, boulex,bouley):
        qp.drawImage(QtCore.QRect(boulex-15 , bouley-38, 15, 15), self.image)
        #print (boulex + 86.2, bouley + 86.20)

if __name__ == '__main__':
    p = Partie (3,0.1)
    Partie.jouer (p)
    #dt = 0.1 #0.2
    #nb_coups = 2
    #c = 0
    #plat = Plateau(mode = 0)
    #for _ in range(nb_coups):# on simule nb_coups coups
    #    plt.figure ()
    #    c += 1
    #    Plateau.un_coup(plat, dt)
    #plt.show()

# trous  --------------->>
# ralentissement des balles  OK
# positionnement initial  -------->>
# en temps réel0
#
#préciser comment éxécuter le code
#graph des classes adapté

#  !! Vmax = 4*R_b/dt
#100 * Cte = Vmax - eps
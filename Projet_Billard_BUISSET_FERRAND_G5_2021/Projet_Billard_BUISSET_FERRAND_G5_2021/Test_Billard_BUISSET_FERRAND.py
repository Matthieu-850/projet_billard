import unittest
import Projet_Billard_BUISSET_FERRAND as pb
import numpy as np


class TestBoule(unittest.TestCase):
    def test_var(self):
        plat = pb.Plateau()
        bou = pb.Boule_blanche(2,3)
        self.assertEqual(bou.x, 2)
        self.assertEqual(bou.y, 3)
        self.assertEqual((bou.vx,bou.vy), (0,0))
        self.assertEqual((plat.bs,plat.bo), (10,0 ))


    def test_type(self):
        bb = pb.Boule_blanche (10, 15, r = 4)
        bc = pb.Boule_coloree (10, 15, r = 4)
        self.assertIsInstance(bb, pb.Boule)
        self.assertIsInstance(bb, pb.Boule)
        self.assertEqual (bb.x,bc.x)


    def test_coords(self):
        bc = pb.Boule_coloree(1, 5)
        bb = pb.Boule_blanche(1, 5)
        self.assertEqual(bc.x, bb.x)
        self.assertEqual(bc.y, bb.y)
        #self.assertIsNot((bc.x, bb.coord)
        # #self.assertIs(bc.coord, bc.coord)
        # ac = bc.coord
        # bc.coord = bc.coord
        # self.assertEqual(bc.coord[0], ac[0])
        # self.assertEqual(bc.coord[1], ac[1])

class TestBouleBlanche(unittest.TestCase):

    def test_type(self):
        bb = pb.Boule_blanche(1, 5)
        self.assertIsInstance(bb, pb.Boule_blanche)
        self.assertIsInstance(bb, pb.Boule)
        bn = pb.Boule_blanche(5, 1)
        self.assertNotIsInstance(bn, pb.Boule_coloree)
        cn = pb.Boule_coloree(2, 2)
        self.assertNotIsInstance(cn, pb.Boule_blanche)

class TestPlateau (unittest.TestCase):
    def test_type(self):
        plat = pb.Plateau (l = 8,L = 15,nb = 10)
        self.assertIsInstance(plat, list)
        bb = pb.Boule_coloree(1, 5)
        plat.append(bb)
        self.assertIs(bb,plat[-1])

        plat1 = pb.Plateau ()
        plat2 = pb.Plateau ()
        self.assertIsNot(plat1.queue, plat2.queue)
        self.assertEqual(plat1.queue.alpha_b, plat2.queue.alpha_b)

class TestPartie (unittest.TestCase):
    def test_var (self):
        partie = pb.Partie (10, ll = 15)
        partie2 = pb.Partie (2)
        self.assertEqual(partie.nb_coups,10)
        self.assertEqual ((partie.plat.bs,partie.plat.bn), (15,0))
        self.assertEqual (partie2.plat[0], partie.plat [0])


    def test_type (self):
        partie1 = pb.Partie(10, ll=15)
        partie2 = pb.Partie(2 )
        self.assertIsNot(partie1.plat.queue, partie2.plat.queue)
        self.assertIsInstance(partie1.plat,pb.Plateau)
        self.assertIsInstance(partie1.plat.queue, pb.Queue)
        self.assertIsNot(partie1.plat[0], partie2.plat[0])


if __name__ == '__main__':
    unittest.main()
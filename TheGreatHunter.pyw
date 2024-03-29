import pyxel
from webbrowser import open
from socket import *
from client import Client
from serveur import Serveur
from music import Music

# Creation Joueur1 (Joueur1)

class Rectangle:
    def __init__(self,x,y,w,h,c):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.c = c
    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, self.c)


class Joueur1:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, colkey=9)


class Joueur2:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 8, 8, 8, colkey=9)


class Jeu:
    def __init__(self, h, l, titre):
        self.block_sans_collision = [(0,0),(5,12),(0,16),(1,16),(0,17),(1,17),(2,16),(3,16),(2,17),(3,17),(1,13),(4,16),(5,16),(4,17),(5,17),(9,16),(9,17)]
        self.block_chache = [(0,16),(1,16),(0,17),(1,17),(2,16),(3,16),(2,17),(3,17)]
        self.imclient = False
        self.timer = 90
        self.code = ""
        self.client = False
        self.serveur = False
        pyxel.init(h, l, title = titre, display_scale=2, fps=60)
        pyxel.fullscreen(False)
        self.plan_x = 0
        self.plan_y = 0
        # charger le rectangle
        self.rectangle = Rectangle(0,0,pyxel.height,pyxel.width,6)
        self.texte = "Appuyez sur la touche 'S' pour etre un Chercheur\nLe code de connexion pour la personne qui se cache est: "+gethostbyname(gethostname())+"\n\nAppuyez sur la touche 'J' pour etre la personne qui se cache\n"
        self.fin = False
        pyxel.load("assets/ress.pyxres")
        # Lancement du jeu
        pyxel.run(self.update, self.draw)

    def update(self):
        #si joueur 1 touche joueur 2
        try:
            if pyxel.frame_count % 60 == 0 and (self.client != False or self.serveur != False) and self.timer > 0 and not self.fin:
                self.timer -= 1
            if (self.Joueur1.x == self.Joueur2.x) and (self.Joueur1.y == self.Joueur2.y):
                self.texte = "Le Chercheur a gagne ! \n\nPour rejouer, appuyez sur la touche 'R'"
                self.rectangle = Rectangle(0,0,pyxel.height,pyxel.width,6)
                self.fin = True
        except:
            pass
        if self.timer <= 0:
            try:
                #je ferme le serveur
                self.serveur.connexion = False
                self.serveur.connexion_avec_client.close()
                #je ferme le client
                self.client.connexion = False
                self.client.client.close()
            except:
                pass
            self.texte = "La personne qui se cache a gagne ! \n\nPour rejouer, appuyez sur la touche 'R'"
            self.rectangle = Rectangle(0,0,pyxel.height,pyxel.width,6)
            self.fin = True
        if self.client:
            try:
                # Je récupère les données du serveur
                player2 = self.client.player2.split(",")
                # Je définis les coordonnées du joueur 2
                x, y = map(int, map(float, player2))
                self.Joueur2 = Joueur1(32, 32)
                self.Joueur2.x = x
                self.Joueur2.y = y
            except:
                pass

        if self.serveur:
            try:
                # Je récupère les données du client
                player2 = self.serveur.player2.split(",")
                # Je définis les coordonnées du joueur 2
                x, y = map(int, map(float, player2))
                self.Joueur2 = Joueur2(384, 320)
                self.Joueur2.x = x
                self.Joueur2.y = y
            except:
                pass
        if self.client:
            try:
                self.client.envoyer("{},{}".format(self.Joueur1.x, self.Joueur1.y))
            except:
                pass
        elif self.serveur:
            try:
                self.serveur.envoyer("{},{}".format(self.Joueur1.x, self.Joueur1.y))
            except:
                pass

        if pyxel.btn(pyxel.KEY_R) and pyxel.btn(pyxel.KEY_I) and pyxel.btn(pyxel.KEY_C) and pyxel.btn(pyxel.KEY_K):
            open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            pyxel.quit()

        #On permet au joueur de rentrer le code (pas natif dans pyxel)
        self.key_dict = {
        pyxel.KEY_0: '0',
        pyxel.KEY_1: '1',
        pyxel.KEY_2: '2',
        pyxel.KEY_3: '3',
        pyxel.KEY_4: '4',
        pyxel.KEY_5: '5',
        pyxel.KEY_6: '6',
        pyxel.KEY_7: '7',
        pyxel.KEY_8: '8',
        pyxel.KEY_9: '9',
        pyxel.KEY_SEMICOLON: '.'
        }

        if self.imclient:
            for key, value in self.key_dict.items():
                if pyxel.btnp(key):
                    self.code += value
                    self.texte += value

            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                self.code = self.code[:-1]
                self.texte = self.texte[:-1]

            if pyxel.btnp(pyxel.KEY_RETURN) and self.code:
                self.texte = ""
                self.client = Client(self.code)
                self.rectangle = Rectangle(0, 0, 0, 0, 0)
        # joueurs Joueur1 designe
        if pyxel.frame_count == 1:
            Music()
        if pyxel.btnp(pyxel.KEY_R) and (self.serveur != False or self.client != False) and self.fin == True:
            #ferme la connection du client et du serveur
            try:
                self.serveur.connexion = False
                self.serveur.connexion_avec_client.close()
                self.client.connexion = False
                self.client.client.close()
            except:
                pass
            self.fin = False
            self.imclient = False
            self.timer = 90
            self.code = ""
            self.client = False
            self.serveur = False
            self.plan_x = 0
            self.plan_y = 0
            self.Joueur1 = Joueur1(-8, -8)
            self.Joueur2 = Joueur2(-16, -16)
            # charger le rectangle
            self.rectangle = Rectangle(0,0,pyxel.height,pyxel.width,6)
            self.texte = "Appuyez sur la touche 'S' pour etre un Chercheur\nLe code de connexion pour la personne qui se cache est: "+gethostbyname(gethostname())+"\n\nAppuyez sur la touche 'J' pour etre la personne qui se cache\n"
            
        if pyxel.btnp(pyxel.KEY_S) and self.serveur == False and self.client == False:
            self.Joueur1 = Joueur1(32, 32)
            self.serveur = Serveur()
            self.rectangle = Rectangle(0,0,0,0,0)
            self.texte = ""
        # joueurs Joueur2 designe
        if pyxel.btnp(pyxel.KEY_J) and self.serveur == False and self.client == False:
            self.Joueur1 = Joueur2(384, 320)
            self.texte = "Tapez le code de connexion du chercheur\n"
            self.imclient = True
        #deplacement avec les touches de direction
        if (self.serveur == False or self.client == False) and self.fin == False:
            try:
                if pyxel.btn(pyxel.KEY_LEFT):
                    for word in self.block_sans_collision:
                        if str(word) in str(pyxel.tilemap(0).pget((self.Joueur1.x-8)/8, self.Joueur1.y/8)):
                            if pyxel.frame_count % 4 == 0:
                                self.Joueur1.x -= 8
                if pyxel.btn(pyxel.KEY_RIGHT):
                    for word in self.block_sans_collision:
                        if str(word) in str(pyxel.tilemap(0).pget((self.Joueur1.x+8)/8, self.Joueur1.y/8)):
                            if pyxel.frame_count % 4 == 0:
                                self.Joueur1.x += 8
                if pyxel.btn(pyxel.KEY_UP):
                    for word in self.block_sans_collision:
                        if str(word) in str(pyxel.tilemap(0).pget(self.Joueur1.x/8, (self.Joueur1.y-8)/8)):
                            if pyxel.frame_count % 4 == 0:
                                self.Joueur1.y -= 8
                if pyxel.btn(pyxel.KEY_DOWN):
                    for word in self.block_sans_collision:
                        if str(word) in str(pyxel.tilemap(0).pget(self.Joueur1.x/8, (self.Joueur1.y+8)/8)):
                            if pyxel.frame_count % 4 == 0:
                                self.Joueur1.y += 8
            except:
                pass
        #Si le joueur un bord de la map, il ne peut pas aller plus loin
        try:
            if self.plan_x == 0:
                if self.Joueur1.x <= 0:
                    self.Joueur1.x = 0
            if self.plan_x == 128:
                if self.Joueur1.x >= 120:
                    self.Joueur1.x = 120
            if self.plan_y == 0:
                if self.Joueur1.y <= 0:
                    self.Joueur1.y = 0
            if self.plan_y == 128:
                if self.Joueur1.y >= 120:
                    self.Joueur1.y = 120
        except:
            pass

    def draw(self):
        pyxel.cls(6)
        pyxel.bltm(0, 0, 0, self.plan_x, self.plan_y, 128*4, 128*4)
        try:
            self.Joueur1.draw()
        except:
            pass
        try:
            self.Joueur2.draw()
        except:
            pass
        self.rectangle.draw()
        pyxel.text(128*2-90, 128*2, self.texte, 0)
        #afficher le timer en haut à gauche
        pyxel.text(2, 2, str(self.timer), 7)

Jeu(128*4, 128*4, "The Great Hunter")
############################
# import et initialisation #
############################

import pygame
import random
import time
import os
from pygame.locals import *

pygame.init()

largeur_fen, hauteur_fen = 800, 600
affi_surface = pygame.display.set_mode((largeur_fen, hauteur_fen))
pygame.display.set_caption("Mon premier jeu !")


############
# Couleurs #
############

blanc = (240, 240, 240)
noir = (20, 20, 20)
corail = (255, 127, 80)
bleu = (100, 149, 237)
gris = (60, 60, 60)


#########
# Texte #
#########


def affiche_texte(taille, message, couleur_texte, pos_x, pos_y,
                  couleur_fond=None):
    fontObj = pygame.font.Font('freesansbold.ttf', taille)
    if couleur_fond:
        textSurfaceObj = fontObj.render(
            message, True, couleur_texte, couleur_fond)
    else:
        textSurfaceObj = fontObj.render(message, True, couleur_texte)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos_x, pos_y)
    affi_surface.blit(textSurfaceObj, textRectObj)


##########
# Bouton #
##########


def affiche_bouton(posx, posy, larg, haut, message,
                   couleur_texte, couleur_fond):
    fond_bouton = pygame.Rect(0, 0, larg, haut)
    fond_bouton.center = (posx, posy)
    pygame.draw.rect(affi_surface, couleur_fond, fond_bouton)
    affiche_texte(32, message, couleur_texte, posx, posy)


def clic_bouton(clicx, clicy, posx, posy, larg, haut):
    dis_x = abs(clicx - posx)
    dis_y = abs(clicy - posy)
    dis_xmax = larg / 2
    dis_ymax = haut / 2
    if (dis_x < dis_xmax) and (dis_y < dis_ymax):
        return True
    else:
        return False


##########
# Images #
##########

fond = pygame.image.load("fond_esp.jpg").convert()
img_vais = pygame.image.load("playerShip1_blue.png").convert_alpha()
img_ast1 = pygame.image.load("asteroid.png").convert_alpha()
img_tir = pygame.image.load("laserBlue01.png").convert_alpha()
img_tir_init = pygame.image.load("fire18.png").convert_alpha()

#########
# Temps #
#########

fps = 30
fps_clock = pygame.time.Clock()

###############
# Le vaisseau #
###############

largeur_vais, hauteur_vais = 99, 75
v_vais = 7


def dessine_vaisseau(x, y):
    affi_surface.blit(img_vais, (x, y))


def position_vaisseau(x, y, x_change, y_change):
    x, y = x + x_change, y + y_change
    if x < 0:
        x = 0
    elif x > largeur_fen - largeur_vais:
        x = largeur_fen - largeur_vais
    if y < 0:
        pygame.quit()
    elif y > hauteur_fen - hauteur_vais:
        y = hauteur_fen - hauteur_vais
    return x, y


#####################
# Gestion asteroids #
#####################

cote_ast = 43
v_ast = 15


def dessine_asteroid(x_ast, y_ast):
    affi_surface.blit(img_ast1, (x_ast, y_ast))


def cree_asteroid():
    return [random.randint(1, largeur_fen - cote_ast - 1), -cote_ast]


def generation_asteroid(asteroids, score):
    if random.random() < 0.1 + score / 1000:
        asteroids.append(cree_asteroid())
    return asteroids


def deplacement_asteroids(asteroids):
    asteroids_poubelle = []
    for asteroid in asteroids:
        asteroid[1] = asteroid[1] + v_ast
        if asteroid[1] + cote_ast > hauteur_fen:
            asteroids_poubelle.append(asteroid)
    for asteroid in asteroids_poubelle:
        asteroids.remove(asteroid)
    return asteroids


########
# Tirs #
########


h_tir = 41
l_tir = 16
v_tir = 30


def affiche_feu_tir(x, y, last_tir):
    if time.time() - last_tir < 0.1 and last_tir != 0:
        affi_surface.blit(img_tir_init, (x - 9 + largeur_vais / 2, y - 38))


def dessine_tir(x_tir, y_tir):
    affi_surface.blit(img_tir, (x_tir, y_tir))


def cree_tir(x, y, tirs, a_tire, last_tir):
    if a_tire:
        tps = time.time()
        if tps - last_tir > 0.2:
            tirs.append([x + (largeur_vais / 2), y - hauteur_vais])
            last_tir = time.time()
    affiche_feu_tir(x, y, last_tir)
    return last_tir, tirs


def deplacement_tirs(tirs):
    tirs_poubelle = []
    for tir in tirs:
        tir[1] = tir[1] - v_tir
        if tir[1] < 0:
            tirs_poubelle.append(tir)
    for tir in tirs_poubelle:
        tirs.remove(tir)
    return tirs


#############
# Collision #
#############


def collision_a_lieu(x_pobj, y_pobj, x_secobj, y_secobj, l_pobj, h_pobj,
                     l_secobj, h_secobj):
    if x_pobj < x_secobj + l_secobj and \
       x_secobj < x_pobj + l_pobj and \
       y_pobj < y_secobj + h_secobj and \
       y_secobj < y_pobj + h_pobj:
        print("collide")
        return True
    return False


def collisions_asteroid_vaisseau(x, y, asteroids, largeur_vais,
                                 hauteur_vais, cote_ast, score):
    for asteroid in asteroids:
        if collision_a_lieu(x, y, asteroid[0], asteroid[1], largeur_vais - 5,
                            hauteur_vais - 5, cote_ast - 5, cote_ast - 5):
            defaite(score)


def collisions_asteroid_tir(asteroids, tirs):
    asteroids_poubelle = []
    tirs_poubelle = []
    for asteroid in asteroids:
        for tir in tirs:
            if collision_a_lieu(tir[0], tir[1], asteroid[0], asteroid[1],
                                l_tir, h_tir, cote_ast, cote_ast):
                asteroids_poubelle.append(asteroid)
                tirs_poubelle.append(tir)
        for tir in tirs_poubelle:
            if tir in tirs:
                tirs.remove(tir)
    for asteroid in asteroids_poubelle:
        asteroids.remove(asteroid)
    return asteroids, tirs

#########
# Score #
#########


def lire_highscore():
    if os.path.exists("highscore.txt"):
        f_score = open("highscore.txt", "r")
        highscore = f_score.read()
        f_score.close()
        return int(highscore)
    else:
        f_score = open("highscore.txt", "w")
        f_score.write(str(0))
        f_score.close()
        return 0


def store_highscore(score):
    highscore = lire_highscore()
    f_score = open("highscore.txt", "r+")
    f_score.write(str(max(score, highscore)))
    f_score.close()


def affiche_score(score, highscore):
    empl_score = 40
    if highscore != 0:
        affiche_texte(30, "Highscore: " + str(highscore), blanc,
                      largeur_fen * 0.84, empl_score)
    affiche_texte(30, "Score: " + str(score), blanc, largeur_fen * 0.1,
                  empl_score)

######################
# Synthèse affichage #
######################


def affiche_tout(tirs, asteroids, score, highscore):
    for tir in tirs:
        dessine_tir(tir[0], tir[1])
    for asteroid in asteroids:
        dessine_asteroid(asteroid[0], asteroid[1])
    affiche_score(score, highscore)


###########
# Défaite #
###########


def defaite(score):
    btn_jouer_centrex = largeur_fen * 0.5
    btn_jouer_centrey = hauteur_fen * 0.75
    btn_jouer_largeur = 150
    btn_jouer_hauteur = 100
    store_highscore(score)
    attente = True
    while attente:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if clic_bouton(event.pos[0], event.pos[1], btn_jouer_centrex,
                               btn_jouer_centrey, btn_jouer_largeur,
                               btn_jouer_hauteur):
                    attente = False
                    jouer()
        affi_surface.blit(fond, (0, 0))
        affiche_texte(32,
                      "Vous avez perdu avec un score de " + str(score),
                      blanc, largeur_fen * 0.5, hauteur_fen * 0.25)
        affiche_bouton(btn_jouer_centrex, btn_jouer_centrey, btn_jouer_largeur,
                       btn_jouer_hauteur, "Rejouer", gris, bleu)
        pygame.display.update()


######################
# La boucle de pause #
#####################

def pause(score):
    en_pause = True
    while en_pause:
        for event in pygame.event.get():
            if event.type == QUIT:
                store_highscore(score)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    en_pause = False
        affi_surface.blit(fond, (0, 0))
        affiche_texte(32, "En pause", blanc, largeur_fen * 0.5,
                      hauteur_fen * 0.55)
        pygame.display.update()


#####################
# La boucle d'intro #
#####################

def intro():
    attente = True
    btn_jouer_centrex = largeur_fen * 0.5
    btn_jouer_centrey = hauteur_fen * 0.75
    btn_jouer_largeur = 150
    btn_jouer_hauteur = 100
    while attente:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    attente = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if clic_bouton(event.pos[0], event.pos[1], btn_jouer_centrex,
                               btn_jouer_centrey, btn_jouer_largeur,
                               btn_jouer_hauteur):
                    attente = False
        affi_surface.fill(blanc)
        affiche_texte(50, "Space blit !", corail,
                      largeur_fen / 2, hauteur_fen * 0.2)
        affiche_bouton(btn_jouer_centrex, btn_jouer_centrey, btn_jouer_largeur,
                       btn_jouer_hauteur, "Jouer", noir, corail)
        dessine_vaisseau((largeur_fen - largeur_vais) / 2, hauteur_fen * 0.3)
        pygame.display.update()

#####################
# La boucle de jeu: #
#####################


def jouer():
    score = 0
    x, y = (largeur_fen - largeur_vais) * 0.5, hauteur_fen * 0.8
    x_change, y_change = 0, 0
    asteroids = []
    tirs = []
    last_tir = 0
    a_tire = False
    highscore = lire_highscore()

    continuons = True
    while continuons:
        for event in pygame.event.get():
            if event.type == QUIT:
                store_highscore(score)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -v_vais
                elif event.key == pygame.K_RIGHT:
                    x_change = v_vais
                elif event.key == pygame.K_UP:
                    y_change = -v_vais
                elif event.key == pygame.K_DOWN:
                    y_change = v_vais
                elif event.key == pygame.K_p:
                    pause(score)
                elif event.key == pygame.K_SPACE:
                    a_tire = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0
                elif event.key == pygame.K_SPACE:
                    a_tire = False
        affi_surface.blit(fond, (0, 0))
        # "Déplacements" du vaisseau
        x, y = position_vaisseau(x, y, x_change, y_change)
        dessine_vaisseau(x, y)
        # "Création et affichage du feu des tirs"
        last_tir, tirs = cree_tir(x, y, tirs, a_tire, last_tir)
        # "Création asteroids"
        asteroids = generation_asteroid(asteroids, score)
        nbr_ast = len(asteroids)
        asteroids = deplacement_asteroids(asteroids)
        tirs = deplacement_tirs(tirs)
        collisions_asteroid_vaisseau(
            x, y, asteroids, largeur_vais, hauteur_vais, cote_ast, score)
        asteroids, tirs = collisions_asteroid_tir(asteroids, tirs)
        nbr_ast_disparu = nbr_ast - len(asteroids)
        score = score + nbr_ast_disparu
        affiche_tout(tirs, asteroids, score, highscore)
        pygame.display.update()
        fps_clock.tick(fps)


intro()
jouer()

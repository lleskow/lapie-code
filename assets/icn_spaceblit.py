############################
# import et initialisation #
############################

import pygame
import random
from pygame.locals import *

pygame.init()

largeur_fen, hauteur_fen = 800, 600
affi_surface = pygame.display.set_mode((largeur_fen, hauteur_fen))
pygame.display.set_caption("Mon premier jeu !")

############
# Couleurs #
############

noir = (0, 0, 0)
blanc = (255, 255, 255)

##########
# Images #
##########

fond = pygame.image.load("fond_esp.jpg").convert()
img_vais = pygame.image.load("playerShip1_blue.png").convert_alpha()

#########
# Temps #
#########

fps = 30
fps_clock = pygame.time.Clock()

#########
# Texte #
#########


def affiche_texte(taille, message, couleur_texte, couleur_fond, pos_x, pos_y):
    fontObj = pygame.font.Font('freesansbold.ttf', taille)
    textSurfaceObj = fontObj.render(message, True, couleur_texte, couleur_fond)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (pos_x, pos_y)
    affi_surface.blit(textSurfaceObj, textRectObj)


###############
# Le vaisseau #
###############


def dessine_vaisseau(x, y):
    affi_surface.blit(img_vais, (x, y))


largeur_vais, hauteur_vais = 99, 75
x, y = (largeur_fen - largeur_vais) * 0.5, hauteur_fen * 0.8
x_change, y_change = 0, 0


def position_vaisseau(x, y):
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
x_ast = random.randint(1, largeur_fen - cote_ast - 1)
y_ast = -cote_ast
v_ast = 15
couleur_ast = (133, 83, 15)


def dessine_asteroid(x_ast, y_ast):
    asteroid = pygame.Rect(x_ast, y_ast, cote_ast, cote_ast)
    pygame.draw.rect(affi_surface, couleur_ast, asteroid)

#############
# Collision #
#############


def collision_a_lieu(x, y, x_ast, y_ast, largeur_vais, hauteur_vais, cote_ast):
    if x < x_ast + cote_ast and \
       x_ast < x + largeur_vais and \
       y < y_ast + cote_ast and \
       y_ast < y + hauteur_vais:
        print("collide")
        return True
    return False

######################
# La boucle de pause #
#####################


#####################
# La boucle d'intro #
#####################


#####################
# La boucle de jeu: #
#####################

continuons = True
while continuons:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -5
            elif event.key == pygame.K_RIGHT:
                x_change = 5
            elif event.key == pygame.K_UP:
                y_change = -5
            elif event.key == pygame.K_DOWN:
                y_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_change = 0
    affi_surface.blit(fond, (0, 0))

    # "Déplacements" du vaisseau
    x, y = position_vaisseau(x, y)
    dessine_vaisseau(x, y)

    # "Déplacements" de l'Asteroid
    y_ast = y_ast + v_ast
    if y_ast > hauteur_fen:
        x_ast = random.randint(1, largeur_fen - cote_ast - 1)
        y_ast = -cote_ast
    dessine_asteroid(x_ast, y_ast)

    # gestion des collisions
    if collision_a_lieu(x, y, x_ast, y_ast,
                        largeur_vais, hauteur_vais, cote_ast):
        print("collision")
        pygame.quit()

    pygame.display.update()
    fps_clock.tick(fps)

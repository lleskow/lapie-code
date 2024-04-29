import pyxel


pyxel.init(128, 128, title="Nuit du c0de")
x_vais, y_vais = 56, 112

def deplacer(dx, dy):
    global x_vais, y_vais
    x_vais += dx
    y_vais += dy


def vaisseau_deplacement():
    """déplacement avec les touches de directions"""
    if pyxel.btn(pyxel.KEY_RIGHT):
        deplacer(1, 0)

def update():
    """mise à jour des variables (30 fois par seconde)"""
    vaisseau_deplacement()


def afficher():
    """ Affiche le vaisseau à l'écran """
    pyxel.rect(x_vais, y_vais, 8, 8, 5)


def draw():
    """ Affiche les éléments dans la fenêtre graphique """
    pyxel.cls(0)
    afficher()


pyxel.run(update, draw)

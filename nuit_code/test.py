import pyxel

pyxel.init(128, 128, title="Nuit du c0de")
pyxel.load("images.pyxres", False, False, True, True)
pyxel.load("1.pyxres", True, True, False, False)
pyxel.playm(0, loop=True)

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
    pyxel.blt(x_vais, y_vais, 0, 0, 0, 8, 8)

def draw():
    """ Affiche les éléments dans la fenêtre graphique """
    pyxel.cls(0)
    afficher()


pyxel.run(update, draw)

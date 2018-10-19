from PIL import Image
from os.path import splitext

def appliquer_fonction_vers_nb(f,image,mode_depart):
    im = Image.open(image)
    largeur, hauteur = im.size
    im2 = Image.new("L",im.size)
    for y in range(hauteur): #parcours des lignes
        for x in range(largeur): #parcours des colonnes d'une ligne
            pixel = im.getpixel((x,y))
            if mode_depart == "L":
                im2.putpixel((x,y),f(pixel))
            else:
                im2.putpixel((x,y),int(f(pixel[0],pixel[1],pixel[2])))
    im2.save(splitext(image)[0]+"new.png")
    print("done")

def appliquer_fonction_vers_couleur(f,image):
    im = Image.open(image)
    largeur, hauteur = im.size
    im2 = Image.new("RGB",im.size)
    for y in range(hauteur): #parcours des lignes
        for x in range(largeur): #parcours des colonnes d'une ligne
            pixel = im.getpixel((x,y))
            im2.putpixel((x,y),tuple(map(int,f(pixel[0],pixel[1],pixel[2]))))
    im2.save(splitext(image)[0]+"new.png")
    print("done")

def appliquer_fonction(f,image):
    try:
        f(1,2,3)
        mode_depart = "RGB"
        if type(f(1,2,3)) != type(1.0) and type(f(1,2,3)) != type(1):
            mode_arrive = "RGB"
        else:
            mode_arrive = "L"
    except:
        f(1)
        mode_depart = "L"
        mode_arrive = "L"
    if mode_arrive == "RGB":
        appliquer_fonction_vers_couleur(f,image)
    else:
        appliquer_fonction_vers_nb(f,image,mode_depart)

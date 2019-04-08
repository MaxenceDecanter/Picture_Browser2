import base64
import io

from PIL import Image


try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3+
    import tkinter as tk


def buildAndReturnLabel(base64i, typeimg):

    received = base64.b64decode(base64i)  # je la decode
    infos = typeimg  # typeimg renvoi l'extension (le format)

    img = Image.open(io.BytesIO(received))  # on ouvre l'image pour la traiter
    if "png" in infos:  # on l'enregistre dans le format correspondant a typeimg
        imgConstruite = "/home/decanter/PycharmProjects/Picture_Browser2/server/test.png"
        img.save(imgConstruite)
    else:
        imgConstruite = "/home/decanter/PycharmProjects/Picture_Browser2/server/test.jpg"
        img.save(imgConstruite)

    return imgConstruite  # on la retourne

import pickle
import xml.etree.cElementTree as ET
class Olimpiada:
    def __init__(self, anio, juegos, temporada, ciudad):
        self.anio= anio
        self.juegos=juegos
        self.temporada=temporada
        self.ciudad=ciudad

    def ver(self):
        print(self.anio + ", "+ self.juegos + ", " + self.temporada + ", " + self.ciudad)



tree = ET.parse('olimpiadas.xml')
root = tree.getroot()

with open('olimpiadas.pickle', 'wb') as f:
    for hijo in root:
        olimpiada=[]
        olimpiada.append(hijo.attrib['year'])

        for nieto in hijo:
            olimpiada.append(nieto.text)

        objOlimpiada = Olimpiada(olimpiada[0], olimpiada[1], olimpiada [2], olimpiada[3])
        pickle.dump(objOlimpiada, f)

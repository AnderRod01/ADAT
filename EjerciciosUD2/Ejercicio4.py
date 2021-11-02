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


def crearSerializableOlimpiadas():
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
    print("Fichero creado correctamente")



def aniadirEdicion():
    anio = input("Año de las olimpiadas: ")
    temporada = input ("Temporada: ")
    ciudad = input("Ciudad: ")

    juegos = anio + " " + temporada


    olimpiadas =[]

    with open('olimpiadas.pickle', 'rb') as f:
        while 1:
            try:
                olimpiada = pickle.load(f)
                olimpiadas.append(olimpiada)
            except EOFError:
                olimpiada =  Olimpiada(anio, juegos, temporada, ciudad)
                olimpiadas.append(olimpiada)
                break

    with open ('olimpiadas.pickle', 'wb') as f:
        for olimpiada in olimpiadas:
            pickle.dump(olimpiada,f)

    #verPickle()

def buscarPorSede():
    sede = input("introduce localizacion de las olimpiadas: ")
    with open ('olimpiadas.pickle', 'rb') as f:
        while 1:
            try:
                olimpiada = pickle.load(f)
                if sede.lower() in olimpiada.ciudad.lower():
                    olimpiada.ver()
            except EOFError:
                break

def eliminarEdicion():
    anio = input("Introduce el año de la olimpiada a eliminar")
    temporada = input ("Introduce la temporada de la olimpiada a eliminar")

    olimpiadas=[]
    with open ('olimpiadas.pickle', 'rb') as f:
        while 1:
            try:
                olimpiada = pickle.load(f)
                olimpiadas.append(olimpiada)
            except EOFError:
                break
    with open ('olimpiadas.pickle', 'wb') as f:
        for olimpiada in olimpiadas:
            if anio != olimpiada.anio and temporada.lower() != olimpiada.temporada.lower():
                pickle.dump(olimpiada, f)

    #verPickle()


def verPickle ():
    with open('olimpiadas.pickle', 'rb') as f:
        while 1:
            try:
                olimpiada = pickle.load(f)
                olimpiada.ver()
            except EOFError:
                break


resp = input('¿Que desea hacer? \n\t1. Crear fichero serializable de olimpiadas\n\t2. Añadir edición olímpica\n\t3. Buscar olimpiadas por sede\n\t4. Eliminar edición olímpica\n\n\t5. Salir\n')
while resp != '5':
    print()
    if resp == '1':
        crearSerializableOlimpiadas()
    elif resp == '2':
        aniadirEdicion()
    elif resp == '3':
        buscarPorSede()
    elif resp == '4':
        eliminarEdicion()
    else:
        print("Opcion inexistente")
    resp = input('¿Que desea hacer? \n\t1. Crear fichero serializable de olimpiadas\n\t2. Añadir edición olímpica\n\t3. Buscar olimpiadas por sede\n\t4. Eliminar edición olímpica\n\n\t5. Salir\n')

import xml.etree.cElementTree as ET
import csv
from xml.dom import minidom
from xml import sax

class Parser(sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""

    def startElement(self, tag, attribute):
        self.CurrentData = tag
        if tag == 'olimpiada':
            print("Olimpiadas de " + attribute["year"])

    def characters(self, content):
        if self.CurrentData == 'juegos':
            print(content)

    def endElement(self, tag):
        self.CurrentData = ""


def crearOlimpiadasXML():

    listaOlimpiadas = []
    with open ('olimpiadas.csv') as csv_file:
        csv_reader=csv.reader(csv_file, delimiter =',')

        primeraLinea= True

        for row in csv_reader:
            if primeraLinea==False:
                listaOlimpiadas.append([row[1], row[0], row[2], row[3]])

            else:
                primeraLinea = False




    listaOlimpiadas = sorted(listaOlimpiadas, key=lambda x: x[2], reverse= True) #ordenar por temporada

    listaOlimpiadas = sorted (listaOlimpiadas, key=lambda y: y[0]) #ordenar por año
    root = ET.Element("Olimpiadas")
    for elemento in listaOlimpiadas:
        olimpiada = ET.SubElement(root, 'olimpiada')
        olimpiada.set('year', str(elemento[0]))
        juegos = ET.SubElement(olimpiada,'juegos')
        juegos.text = elemento[1]
        temporada = ET.SubElement(olimpiada, 'temporada')
        temporada.text = elemento[2]
        ciudad = ET.SubElement(olimpiada, 'ciudad')
        ciudad.text = elemento[3]

    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open("olimpiadas.xml", "w") as f:
        f.write(xmlstr)


def crearDeportistasXML():
    diccionario = {}

    with open ("atletas.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        root = ET.Element("Deportistas")




        primeraLinea = True
        for row in csv_reader:
            if primeraLinea == False:
                listaClaves = diccionario.keys()
                if row[0] not in listaClaves:
                    deportista = ET.SubElement(root,"Deportista", id=row[0])

                    nombre = ET.SubElement(deportista, "Nombre").text = row[1]
                    sexo = ET.SubElement(deportista, "Sexo").text = row[2]
                    altura = ET.SubElement(deportista, "Altura").text = row[4]
                    peso = ET.SubElement(deportista, "Peso").text = row[5]

                    participaciones = ET.SubElement(deportista, "participaciones")

                    listaDeporte = []
                else:
                    listaDeporte = diccionario.get(row[0])

                deporte = ET.SubElement(participaciones, 'deporte', nombre=row[12])
                listaDeporte.append(row[12])
                diccionario[row[0]] = listaDeporte

                participacion = ET.SubElement(deporte, "Participacion", edad=row[3])

                equipo = ET.SubElement(participacion, "Equipo", abbr=row[7]).text = row[6]
                juegos = ET.SubElement(participacion, "Juegos").text = row[8] + " - " + row[11]
                evento = ET.SubElement(participacion, "Evento").text = row[13]
                medalla = ET.SubElement(participacion, "Medalla").text = row[14]
            else:
                primeraLinea = False






        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open("deportistas.xml", "w") as f:
            f.write(xmlstr)

def verOlimpiadas():
    parser = sax.make_parser()
    parser.setFeature(sax.handler.feature_namespaces, 0)
    handler = Parser()
    parser.setContentHandler(handler)
    parser.parse("olimpiadas.xml")

resp = input('¿Que desea hacer? \n\t1. Crear fichero XML de olimpiadas\n\t2. Crear fichero XML de deportistas\n\t3. Listado de olimpiadas\n\n\t4. Salir\n')
while resp != '4':
    print()
    if resp == '1':
        crearOlimpiadasXML()
    elif resp == '2':
        crearDeportistasXML()
    elif resp == '3':
        verOlimpiadas()
    else:
        print("No existe esa opcion")
    resp = input('¿Que desea hacer? \n\t1. Crear fichero XML de olimpiadas\n\t2. Crear fichero XML de deportistas\n\t3. Listado de olimpiadas\n\n\t4. Salirn')





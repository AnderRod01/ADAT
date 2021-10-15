import xml.etree.cElementTree as ET
import csv
from xml.dom import minidom

'''
with open ('Olimpiadas.csv') as csv_file:
    csv_reader=csv.reader(csv_file, delimiter =',')

    root = ET.Element("Olimpiadas")

    primeraLinea= True

    for row in csv_reader:

        if primeraLinea==False:
            olimpiada = ET.SubElement(root, "Olimpiada", year=row[0])

            juegos = ET.SubElement(olimpiada, "Juegos").text = row[1]
            temporada = ET.SubElement(olimpiada, "Temporada").text = row[2]
            ciudad = ET.SubElement(olimpiada, "Ciudad").text = row[3]

        primeraLinea=False

    tree = ET.ElementTree(root)
    tree.write("olimpiadas.xml")

'''



with open ("atletas.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    root = ET.Element("Deportistas")



    id=0
    primeraLinea = True
    for row in csv_reader:
        if primeraLinea == False:

            if id!= int(row[0]):

                id = int(row[0])
                deportista = ET.SubElement(root,"Deportista", id=row[0])

                nombre = ET.SubElement(deportista, "Nombre").text = row[1]
                sexo = ET.SubElement(deportista, "Sexo").text = row[2]
                altura = ET.SubElement(deportista, "Altura").text = row[4]
                peso = ET.SubElement(deportista, "Peso").text = row[5]

                participaciones = ET.SubElement(deportista, "Participaciones")

                for deporte in participaciones:
                    deporte = ET.SubElement(participaciones, "Deporte", nombre=row[12])



        primeraLinea = False


    '''
        participacion = ET.SubElement(deporte, "Participacion", edad=row[3])

        equipo = ET.SubElement(participacion, "Equipo", abbr = row[7]).text = row[6]
        juegos = ET.SubElement(participacion, "Juegos").text= row[8] + " - " + row[11]
        evento = ET.SubElement(participacion, "Evento").text = row[13]
        medalla = ET.SubElement(participacion, "Medalla").text = row[14]
        
        
    '''

    tree = ET.ElementTree(root)
    tree.write("Atletas.xml")





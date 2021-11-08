import mysql.connector as mysql
import csv
import time
import sqlite3
import xml.etree.cElementTree as ET


dicOlimpiadas = {}
dicEquipos = {}
dicDeportistas = {}
dicDeportes = {}
dicEventos = {}
dicParticipaciones = {}

def cargarDatosCSV ():


    f = input("Introduce el nombre del fichero .csv")

    try:
        with open(f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_file.readline()
            idOlimpiada = 1
            idEquipo = 1
            idDeporte = 1
            idEvento = 1

            idOlimAct = ""
            idDeportistaAct = ""
            idEquipoAct = ""
            idDeporteAct = ""
            idEventoAct = ""

            for row in csv_reader:

                if row[8] not in dicOlimpiadas:
                    idOlimAct = idOlimpiada
                    olimpiada = [idOlimAct, row[8], row[9], row[10], row[11]]
                    dicOlimpiadas[row[8]] = olimpiada
                    idOlimpiada = idOlimpiada + 1
                else:
                    idOlimAct = dicOlimpiadas[row[8]][0]

                if row[0] not in dicDeportistas:
                    deportista = [row[0], row[1], row[2], row[4], row[5]]
                    dicDeportistas[row[0]] = deportista
                    idDeportistaAct = row[0]
                    if row[4] == "NA":
                        dicDeportistas[row[0]][3] = None
                    if row[5] == "NA":
                        dicDeportistas[row[0]][4] = None
                else:
                    idDeportistaAct = dicDeportistas[row[0]][0]

                if row[6] not in dicEquipos:
                    idEquipoAct = idEquipo
                    equipo = [idEquipoAct, row[6], row[7]]
                    dicEquipos[row[6]] = equipo
                    idEquipo += 1
                else:
                    idEquipoAct = dicEquipos[row[6]][0]

                if row[12] not in dicDeportes:
                    idDeporteAct = idDeporte
                    deporte = [idDeporteAct, row[12]]
                    dicDeportes[row[12]] = deporte
                    idDeporte += 1
                else:
                    idDeporteAct = dicDeportes[row[12]][0]

                claveEvento = str(idOlimAct) + "" + row[13]
                if claveEvento not in dicEventos:
                    idEventoAct = idEvento
                    evento = [idEventoAct, row[13], idOlimAct, idDeporteAct]
                    dicEventos[claveEvento] = evento
                    idEvento += 1
                else:
                    idEventoAct = dicEventos[claveEvento][0]

                claveParticipacion = str(idDeportistaAct) + "" + str(idEventoAct) + "" + str(idEquipoAct)
                if claveParticipacion not in dicParticipaciones:
                    participacion = [idDeportistaAct, idEventoAct, idEquipoAct, row[3], row[14]]
                    dicParticipaciones[claveParticipacion] = participacion
                    if row[3] == "NA":
                        dicParticipaciones[claveParticipacion][3] = None

            print("diccionarios cargados")
    except FileNotFoundError as fnfe:
        print("El archivo csv no existe")





def cargarMySQL():

    cargarDatosCSV()

    try:
        cn = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password")

        if cn.is_connected():
            cursor = cn.cursor()

            deleteParticipacion = "drop table if exists Participacion"
            deleteEvento = "drop table if exists Evento"
            deleteDeporte = "drop table if exists Deporte"
            deleteDeportista = "drop table if exists Deportista"
            deleteOlimpiada = "drop table if exists Olimpiada"
            deleteEquipo = "drop table if exists Equipo"

            cursor.execute(deleteParticipacion)
            cursor.execute(deleteEvento)
            cursor.execute(deleteDeporte)
            cursor.execute(deleteDeportista)
            cursor.execute(deleteEquipo)
            cursor.execute(deleteOlimpiada)

            cn.commit()
            print("borrado")
            #
            f = open ('olimpiadas.sql', 'r')

            sqlFile = f.read()
            f.close()
            sqlCommands = sqlFile.split(';')



            for command in sqlCommands:
                cursor.execute(command)

            cn.commit()
            print("tablas creadas")


            query = "Insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (%s, %s, %s, %s, %s)"
            cursor.executemany(query, list(dicOlimpiadas.values()))

            print("olimpiadas cargadas")


            cn.commit()

            query = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
            cursor.executemany(query, list(dicEquipos.values()))

            print("equipos cargados")
            cn.commit()


            query = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
            cursor.executemany(query, list(dicDeportistas.values()))



            print("deportistas cargados")
            cn.commit()


            query = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
            cursor.executemany(query, list(dicDeportes.values()))

            print("deportes cargados")
            cn.commit()



            query = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (%s,%s,%s,%s)"
            cursor.executemany(query, list(dicEventos.values()))
            print("eventos cargados")
            cn.commit()



            query = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (%s,%s,%s,%s,%s)"
            cursor.executemany(query, list(dicParticipaciones.values()))
            print("Participaciones cargadas")
            cn.commit()

            print("La carga de la información se ha realizado correctamente")

    except Exception as e:
        print ("Ha ocurrido algun error en la carga")
        cursor.close()






def cargarSQLite ():
    cn = sqlite3.connect('olimpiadas.db')
    cargarDatosCSV()

    try:
        cursor = cn.cursor()

        f = open('olimpiadas.db.sql', 'r')

        sqlFile = f.read()
        f.close()
        sqlCommands = sqlFile.split(';')

        for command in sqlCommands:
            cursor.execute(command)

        cn.commit()
        print("tablas creadas")

        query = "Insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (?,?,?,?,?)"
        cursor.executemany(query, list(dicOlimpiadas.values()))

        print("olimpiadas cargadas")

        cn.commit()

        query = "Insert into Equipo (id_equipo, nombre, iniciales) values (?,?,?)"
        cursor.executemany(query, list(dicEquipos.values()))

        print("equipos cargados")
        cn.commit()

        query = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (?,?,?,?,?)"
        cursor.executemany(query, list(dicDeportistas.values()))

        print("deportistas cargados")
        cn.commit()

        query = "Insert into Deporte (id_deporte, nombre) values (?,?)"
        cursor.executemany(query, list(dicDeportes.values()))

        print("deportes cargados")
        cn.commit()

        query = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (?,?,?,?)"
        cursor.executemany(query, list(dicEventos.values()))
        print("eventos cargados")
        cn.commit()

        query = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (?,?,?,?,?)"
        cursor.executemany(query, list(dicParticipaciones.values()))
        print("Participaciones cargadas")
        cn.commit()

        print("La carga de la información se ha realizado correctamente")

    except Exception as e:
        print("Ha ocurrido algun error en la carga")
        cn.close()


def mostrarParticipantes():
    bbdd=input("MySQL o SQLite?")

    if (bbdd.lower()=="mysql"):
        cn = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password")
        cursor= cn.cursor()
        temp = input("Winter o Summer? (W/S")

        if (temp == 'W'):
            query = "select * from Olimpiada where Olimpiada.temporada = 'Winter'"
            print(cursor.execute(query))


            edicion = input("Elige la edicion olimpica (id)")

            query = "select * from Deporte where "
            deporte = input("Elige deporte (id)")

            evento = input("Elige evento (id)")





    else:
        cn = sqlite3.connect('olimpiadas.db')



tic= time.perf_counter()
# cargarMySQL()
mostrarParticipantes()

toc = time.perf_counter()
print(f"Build finished in {(toc - tic)/60:0.0f} minutes {(toc - tic)%60:0.0f} seconds")
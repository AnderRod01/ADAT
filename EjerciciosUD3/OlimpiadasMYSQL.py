import mysql.connector as mysql
import csv
import time
import sqlite3


def cargarDatosMySQL():
    dicOlimpiadas={}
    dicEquipos={}
    dicDeportistas={}
    dicDeportes={}
    dicEventos={}
    dicParticipaciones={}

    f = input ("Introduce el nombre del fichero .csv")

    try:
        with open (f) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_file.readline()
            idOlimpiada = 1
            idEquipo = 1
            idDeporte = 1
            idEvento = 1


            idOlimAct = ""
            idDeportistaAct= ""
            idEquipoAct =""
            idDeporteAct=""
            idEventoAct=""

            for row in csv_reader:


                if row[8] not in dicOlimpiadas:
                    idOlimAct = idOlimpiada
                    olimpiada = [idOlimAct, row[8], row[9], row[10], row[11]]
                    dicOlimpiadas[row[8]]=olimpiada
                    idOlimpiada=idOlimpiada+1
                else:
                    idOlimAct = dicOlimpiadas[row[8]][0]




                if row[0] not in dicDeportistas:
                    deportista = [row[0], row[1], row[2], row[4], row[5]]
                    dicDeportistas[row[0]]=deportista
                    idDeportistaAct= row[0]
                    if row[4] == "NA":
                        dicDeportistas[row[0]][3]=None
                    if row[5] == "NA":
                        dicDeportistas[row[0]][4]=None
                else:
                    idDeportistaAct = dicDeportistas[row[0]][0]


                if row[6] not in dicEquipos:
                    idEquipoAct = idEquipo
                    equipo = [idEquipoAct,row[6], row[7]]
                    dicEquipos[row[6]]= equipo
                    idEquipo+=1
                else:
                    idEquipoAct=dicEquipos[row[6]][0]




                if row[12] not in dicDeportes:
                    idDeporteAct = idDeporte
                    deporte = [idDeporteAct,row[12]]
                    dicDeportes[row[12]]=deporte
                    idDeporte+=1
                else:
                    idDeporteAct=dicDeportes[row[12]][0]





                claveEvento = str(idOlimAct) + "" + row[13]
                if claveEvento not in dicEventos:
                    idEventoAct=idEvento
                    evento = [idEventoAct,row[13], idOlimAct, idDeporteAct]
                    dicEventos[claveEvento]=evento
                    idEvento+=1
                else:
                    idEventoAct=dicEventos[claveEvento][0]




                claveParticipacion=str(idDeportistaAct)+""+str(idEventoAct)+""+str(idEquipoAct)
                if claveParticipacion not in dicParticipaciones:
                    participacion = [idDeportistaAct, idEventoAct, idEquipoAct, row[3], row[14]]
                    dicParticipaciones[claveParticipacion]=participacion
                    if row[3]=="NA":
                        dicParticipaciones[claveParticipacion][3] = None

            print("diccionarios cargados")

            try:
                cn = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password", autocommit=True)

                if cn.is_connected():
                    cursor = cn.cursor()

                    # deleteParticipacion = "drop table if exists Participacion"
                    # deleteEvento = "drop table if exists Evento"
                    # deleteDeporte = "drop table if exists Deporte"
                    # deleteDeportista = "drop table if exists Deportista"
                    # deleteOlimpiada = "drop table if exists Olimpiada"
                    # deleteEquipo = "drop table if exists Equipo"
                    deleteParticipacion = "delete from Participacion"
                    deleteEvento = "delete from  Evento"
                    deleteDeporte = "delete from Deporte"
                    deleteDeportista = "delete from  Deportista"
                    deleteOlimpiada = "delete from  Olimpiada"
                    deleteEquipo = "delete from  Equipo"
                    cursor.execute(deleteParticipacion)
                    cursor.execute(deleteEvento)
                    cursor.execute(deleteDeporte)
                    cursor.execute(deleteDeportista)
                    cursor.execute(deleteEquipo)
                    cursor.execute(deleteOlimpiada)

                    print("borrado")


                    # createDeporte= "CREATE TABLE `Deporte` (`id_deporte` int(11) NOT NULL,`nombre` varchar(100) COLLATE latin1_spanish_ci NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci"
                    # cursor.execute(createDeporte)
                    #
                    # createDeportista = "CREATE TABLE `Deportista` (`id_deportista` int(11) NOT NULL,`nombre` varchar(150) COLLATE latin1_spanish_ci NOT NULL,`sexo` enum('M','F') COLLATE latin1_spanish_ci NOT NULL,`peso` int(11) DEFAULT NULL,`altura` int(11) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci"
                    # cursor.execute(createDeportista)
                    #
                    # createEquipo = "CREATE TABLE `Equipo` (`id_equipo` int(11) NOT NULL, `nombre` varchar(50) COLLATE latin1_spanish_ci NOT NULL, `iniciales` varchar(3) COLLATE latin1_spanish_ci NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;"
                    # cursor.execute(createEquipo)
                    #
                    # createEvento = "CREATE TABLE `Evento` (`id_evento` int(11) NOT NULL,`nombre` varchar(150) NOT NULL,`id_olimpiada` int(11) NOT NULL,`id_deporte` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_spanish_ci;"
                    # cursor.execute(createEvento)
                    #
                    # createOlimpiada =


                    query = "Insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (%s, %s, %s, %s, %s)"
                    cursor.executemany(query, list(dicOlimpiadas.values()))

                    print("olimpiadas cargadas")




                    query = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
                    cursor.executemany(query, list(dicEquipos.values()))

                    print("equipos cargados")


                    query = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
                    cursor.executemany(query, list(dicDeportistas.values()))



                    print("deportistas cargados")


                    query = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
                    cursor.executemany(query, list(dicDeportes.values()))

                    print("deportes cargados")



                    query = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (%s,%s,%s,%s)"
                    cursor.executemany(query, list(dicEventos.values()))
                    print("eventos cargados")



                    query = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (%s,%s,%s,%s,%s)"
                    cursor.executemany(query, list(dicParticipaciones.values()))
                    print("Participaciones cargadas")

                    print("La carga de la información se ha realizado correctamente")

            except Exception as e:
                print ("Ha ocurrido algun error en la carga")
    except FileNotFoundError as fnfe:
        print("El archivo csv no existe")


def cargarDatosSQLite ():
    cn = sqlite3.connect('olimpiadas.db')






tic= time.perf_counter()
cargarDatosMySQL()


toc = time.perf_counter()
print(f"Build finished in {(toc - tic)/60:0.0f} minutes {(toc - tic)%60:0.0f} seconds")
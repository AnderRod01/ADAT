import mysql.connector as mysql
import csv
import time


def cargarDatos():
    dicOlimpiadas={}
    dicEquipos={}
    dicDeportistas={}
    dicDeportes={}
    dicEventos={}
    dicParticipaciones={}


    with open('athlete_events.csv') as csv_file:
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

            # if olimpiada not in dicOlimpiadas.values():
            if row[8] not in dicOlimpiadas:
                # dicOlimpiadas[idOlimpiada]=olimpiada
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




            # contDeporte=1
            # for deporteEvento in dicDeportes.values():
            #     if (deporteEvento == deporte):
            #         break
            #     else:
            #         contDeporte+=1

            # contOlimpiada=1
            # for olimpiadaEvento in dicOlimpiadas.values():
            #     if (olimpiadaEvento==olimpiada):
            #         break
            #     else:
            #         contOlimpiada+=1

            claveEvento = str(idOlimAct) + "" + row[13]
            if claveEvento not in dicEventos:
                idEventoAct=idEvento
                evento = [idEventoAct,row[13], idOlimAct, idDeporteAct]
                dicEventos[claveEvento]=evento
                idEvento+=1
            else:
                idEventoAct=dicEventos[claveEvento][0]



            # contDeportista = 1
            # for deportistaPart in dicDeportistas.values():
            #     if (deportistaPart == deportista):
            #         break
            #     else:
            #         contDeportista += 1

            # contEvento =1
            # for eventoPart in dicParticipaciones.values():
            #     if (eventoPart == evento):
            #         break
            #     else:
            #         contEvento+=1

            # contEquipo = 1
            # for equipoPart in dicEquipos.values():
            #     if (equipoPart ==equipo):
            #         break
            #     else:
            #         contEquipo+=1

            claveParticipacion=str(idDeportistaAct)+""+str(idEventoAct)+""+str(idEquipoAct)
            if claveParticipacion not in dicParticipaciones:
                participacion = [idDeportistaAct, idEventoAct, idEquipoAct, row[3], row[14]]
                dicParticipaciones[claveParticipacion]=participacion
                if row[3]=="NA":
                    dicParticipaciones[claveParticipacion][3] = None

        print("diccionarios cargados")
        cn = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password", autocommit=True)

        if cn.is_connected():
            cursor = cn.cursor()

            deleteParticipacion = "delete from Participacion"
            deleteEvento = "delete from Evento"
            deleteDeporte = "delete from Deporte"
            deleteDeportista = "delete from Deportista"
            deleteOlimpiada = "delete from Olimpiada"
            deleteEquipo = "delete from Equipo"
            cursor.execute(deleteParticipacion)
            cursor.execute(deleteEvento)
            cursor.execute(deleteDeporte)
            cursor.execute(deleteDeportista)
            cursor.execute(deleteEquipo)
            cursor.execute(deleteOlimpiada)



            # listaAux = []
            # for datos in dicOlimpiadas:
            #     listaAux.append(list(dicOlimpiadas.get(datos)))
            query = "Insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (%s, %s, %s, %s, %s)"
            cursor.executemany(query, list(dicOlimpiadas.values()))

            print("olimpiadas cargadas")


            # listaAux = []
            # for datos in dicEquipos:
            #     listaAux.append(list(dicEquipos.get(datos)))
            query = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
            cursor.executemany(query, list(dicEquipos.values()))

            print("equipos cargados")

            # query = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
            # cursor.executemany(query, dicEquipos.values())

            # listaAux = []
            # for datos in dicDeportistas:
            #     listaAux.append(list(dicDeportistas.get(datos)))
            query = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
            cursor.executemany(query, list(dicDeportistas.values()))
            # query = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
            # cursor.executemany(query, dicDeportistas.values())

            print("deportistas cargados")

            # listaAux = []
            # for datos in dicDeportes:
            #     listaAux.append(list(dicDeportes.get(datos)))
            query = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
            cursor.executemany(query, list(dicDeportes.values()))

            print("deportes cargados")

            # query = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
            # cursor.executemany(query,dicDeportes.values())

            # listaAux = []
            # for datos in dicEventos:
            #     listaAux.append(list(dicEventos.get(datos)))
            query = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (%s,%s,%s,%s)"
            cursor.executemany(query, list(dicEventos.values()))
            print("eventos cargados")

            # listaAux= []
            # for datos in dicParticipaciones:
            #     listaAux.append(list(dicParticipaciones.get(datos)))

            query = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values (%s,%s,%s,%s,%s)"
            cursor.executemany(query, list(dicParticipaciones.values()))
            print("Participaciones cargadas")

        #print(dicEventos)
        #print(dicParticipaciones)

tic= time.perf_counter()
cargarDatos()
print("La carga de la información se ha realizado correctamente")

toc = time.perf_counter()
print(f"Build finished in {(toc - tic)/60:0.0f} minutes {(toc - tic)%60:0.0f} seconds")
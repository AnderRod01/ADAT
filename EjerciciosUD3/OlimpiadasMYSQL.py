import mysql.connector as mysql
import csv

def cargarDatos():
    dicOlimpiadas={}
    dicEquipos={}
    dicDeportistas={}
    dicDeportes={}
    dicEventos={}
    dicParticipaciones={}


    with open('athlete_events_recortado.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        idOlimpiada = 1
        idEquipo = 1
        idDeportista = 1
        idDeporte = 1
        idEvento = 1
        idParticipacion = 1
        primeraLinea=True
        for row in csv_reader:

            if primeraLinea:
                primeraLinea=False
            else:
                olimpiada= [row[8], row[9], row[10], row[11]]
                if olimpiada not in dicOlimpiadas.values():
                    dicOlimpiadas[idOlimpiada]=olimpiada
                    idOlimpiada=idOlimpiada+1


                deportista = [row[1], row[2], row[4], row[5]]
                if deportista not in dicDeportistas.values():
                    dicDeportistas[idDeportista]=deportista
                    idDeportista+=1


                equipo = [row[6], row[7]]
                if equipo not in dicEquipos.values():
                    dicEquipos[idEquipo]= equipo
                    idEquipo+=1


                deporte = [row[12]]
                if deporte not in dicDeportes.values():
                    dicDeportes[idDeporte]=deporte
                    idDeporte+=1




                contDeporte=1
                for deporteEvento in dicDeportes.values():
                    if (deporteEvento == deporte):
                        break
                    else:
                        contDeporte+=1

                contOlimpiada=1
                for olimpiadaEvento in dicOlimpiadas.values():
                    if (olimpiadaEvento==olimpiada):
                        break
                    else:
                        contOlimpiada+=1

                evento = [row[13], contOlimpiada, contDeporte]
                if evento not in dicEventos.values():
                    dicEventos[idEvento]=evento
                    idEvento+=1




                contDeportista = 1
                for deportistaPart in dicDeportistas.values():
                    if (deportistaPart == deportista):
                        break
                    else:
                        contDeportista += 1

                contEvento =1
                for eventoPart in dicParticipaciones.values():
                    if (eventoPart == evento):
                        break
                    else:
                        contEvento+=1

                contEquipo = 1
                for equipoPart in dicEquipos.values():
                    if (equipoPart ==equipo):
                        break
                    else:
                        contEquipo+=1


                participacion = [contDeportista, contEvento, contEquipo, row[3], row[14]]
                if participacion not in dicParticipaciones.values():
                    dicParticipaciones[idParticipacion]=participacion
                    idParticipacion+=1


        cn = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password", autocommit=False)

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


            for id in dicOlimpiadas:
                query = "Insert into Olimpiada (id_olimpiada,nombre,anio,temporada,ciudad) values (%s, %s, %s, %s, %s)"
                datos = dicOlimpiadas.get(id)
                datosAInsertar = [id, datos[0], datos[1], datos[2], datos[3]]
                cursor.execute(query, datosAInsertar)




            for id in dicEquipos:
                query = "Insert into Equipo (id_equipo, nombre, iniciales) values (%s, %s, %s)"
                datos = dicEquipos.get(id)
                datosAInsertar = [id, datos[0], datos[1]]
                cursor.execute(query, datosAInsertar)


            for id in dicDeportistas:
                query = "Insert into Deportista (id_deportista, nombre, sexo, peso, altura) values (%s, %s, %s, %s, %s)"
                datos = dicDeportistas.get(id)
                if datos[2]=="NA":
                    datos[2]=None
                if datos[3] == "NA":
                    datos[3] = None
                datosAInsertar = [id, datos[0], datos[1], datos[2], datos[3]]
                cursor.execute(query, datosAInsertar)

            for id in dicDeportes:
                query = "Insert into Deporte (id_deporte, nombre) values (%s,%s)"
                datos = dicDeportes.get(id)
                datosAInsertar=[id, datos[0]]
                cursor.execute(query, datosAInsertar)

            for id in dicEventos:
                query = "insert into Evento (id_evento, nombre, id_olimpiada, id_deporte) values (%s,%s,%s,%s)"
                datos = dicEventos.get(id)
                datosAInsertar= [id, datos[0], datos[1], datos[2]]
                cursor.execute(query, datosAInsertar)


            for id in dicParticipaciones:
                query = "insert into Participacion values (%s,%s,%s,%s,%s)"
                datos = dicParticipaciones.get(id)
                if datos[3] == "NA":
                    datos[3] = None
                datosAInsertar= [datos[0],datos[1],datos[2],datos[3],datos[4]]
                cursor.execute(query, datosAInsertar)

        cn.commit()
        #print(dicEventos)
        #print(dicParticipaciones)


cargarDatos()
print("La carga de la información se ha realizado correctamente")






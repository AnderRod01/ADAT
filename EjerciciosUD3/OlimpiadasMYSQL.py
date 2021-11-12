from _curses import curs_set

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
    else:
        cn = sqlite3.connect('olimpiadas.db')

    cursor= cn.cursor()
    temp = input("Winter o Summer? (W/S)")
    while (temp.lower() != 'w' and temp.lower()!= 's'):
        temp = input("Debes introducir W o S")


    if (temp.lower() == 'w'):
        temp = "Winter"
    else:
        temp="Summer"


    query = "select id_olimpiada, nombre from Olimpiada where Olimpiada.temporada = '" + temp + "'"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(str(row[0]) + ' - ' +row[1])
    edicion = input("Elige la edicion olimpica (id)")


    query = "select id_deporte, nombre from Deporte where exists " \
            "(select * from Evento where Deporte.id_deporte = Evento.id_deporte and id_olimpiada = " + edicion + ")"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(str(row[0]) + ' - ' + row[1])
    deporte = input("Elige deporte (id)")


    query = "select id_evento, nombre from Evento where id_olimpiada = " + edicion + " and id_deporte = " + deporte
    cursor.execute(query)
    for row in cursor.fetchall():
        print(str(row[0]) + ' - ' + row[1])
    evento = input("Elige evento (id)")



    query = "select o.temporada, o.nombre, d.nombre, e.nombre from Olimpiada o, Deporte d, Evento e where " \
            "o.id_olimpiada = e.id_olimpiada and " \
            "d.id_deporte = e.id_deporte and " \
            "e.id_evento = " + evento
    cursor.execute(query)
    for row in cursor.fetchall():
        print ("=" * 50)
        print (row[1] + '\t' + row[1] + '\t' + row[2] + '\t' + row[3])
        print ("=" * 50)



    query = "select d.nombre, d.altura, d.peso, p.edad, e.nombre, p.medalla from Deportista d, Participacion p, Equipo e where " \
            "p.id_deportista = d.id_deportista and " \
            "p.id_equipo = e.id_equipo and " \
            "p.id_evento = " + evento

    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)


def deportistaEnDeportes():
    bbdd = input("MySQL o SQLite?")

    if (bbdd.lower() == "mysql"):
        cn = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password")
    else:
        cn = sqlite3.connect('olimpiadas.db')

    cursor = cn.cursor()

    query = "select dsta.nombre, dsta.sexo, dsta.altura, dsta.peso, dte.nombre, p.edad, ev.nombre, eq.nombre, o.nombre, p.medalla " \
             "from Deporte dte, Participacion p, Equipo eq, Evento ev, Olimpiada o, Deportista dsta " \
             "where p.id_evento = ev.id_evento " \
             "and p.id_equipo = eq.id_equipo " \
             "and ev.id_deporte = dte.id_deporte " \
             "and ev.id_olimpiada = o.id_olimpiada " \
             "and p.id_deportista = dsta.id_deportista " \
             "and (select count(distinct (dte2.id_deporte)) from Deporte dte2, Evento ev2, Participacion p2  " \
             "  where dte2.id_deporte = ev2.id_deporte " \
             "  and p2.id_evento = ev2.id_evento " \
             "  and p2.id_deportista = dsta.id_deportista) > 1"

    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)


def modMedalla ():
    cn1 = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password")
    cn2 =  sqlite3.connect('olimpiadas.db')
    cursor1 = cn1.cursor()
    cursor2 = cn2.cursor()

    nombre = input("Introduce nombre de deportista")
    query = "select * from Deportista where nombre like '%" + nombre + "%'"

    cursor1.execute(query)
    for row in cursor1.fetchall():
        print(str(row[0]) + " - " + row[1])

    deportista = input ("Introduce id de deportista")

    query = "select * from Evento where exists " \
            "(select * from Participacion where Evento.id_evento = Participacion.id_evento and Participacion.id_deportista =" + deportista + ")"

    cursor1.execute(query)
    for row in cursor1.fetchall():
        print(str(row[0]) + " - " + row[1])

    evento = input("Introduce id de evento")

    medalla = input("Introduce nuevo valor para medalla (Gold, Silver,Bronze,NA)")
    while (medalla.lower() != 'gold' and medalla.lower() != 'silver' and medalla.lower() != 'bronze' and medalla.lower() != 'na'):
        medalla = input("Debes introducir Gold, Silver, Bronze o NA")


    query = "update Participacion set medalla = '"+ medalla + "' where " \
            "id_deportista = '" + deportista + "' and id_evento = '" + evento + "'"

    cursor1.execute(query)
    cursor2.execute(query)
    cn1.commit()
    cn2.commit()


    print("Medalla actualizada correctamente")


def aniadirDeportistaParticipacion ():
    cn1 = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password")
    cn2 = sqlite3.connect('olimpiadas.db')
    cursor1 = cn1.cursor()
    cursor2 = cn2.cursor()

    nombre = input("Introduce nombre de deportista")
    query = "select * from Deportista where nombre like '%" + nombre + "%'"

    cursor1.execute(query)

    listaDeportistas = []
    for row in cursor1.fetchall():
        listaDeportistas.append(row)
        print(str(row[0]) + " - " + row[1])
    if(len(listaDeportistas) == 0):

        query = "select * from Deportista ORDER BY id_deportista DESC LIMIT 1"
        cursor1.execute(query)
        for row in cursor1.fetchall():
            id = row[0] + 1

        sexo = input("Introduce sexo del deportista")
        while (sexo.lower() != 'm' and sexo.lower() != 'f'):
            sexo = input("Debes introducir M o F")


        peso = input ("Introduce peso del deportista")
        altura = input("Introduce altura del deportista")

        query = "insert into Deportista (id_deportista, nombre, sexo, peso, altura) values " \
                "(" + str(id) + ", '" + nombre + "', '" + sexo + "', " + str(peso) + ", " + str(altura) +")"
        cursor1.execute(query)
        cursor2.execute(query)
        cn1.commit()
        cn2.commit()




        temp = input("Winter o Summer? (W/S)")
        while (temp.lower() != 'w' and temp.lower() != 's'):
            temp = input("Debes introducir W o S")

        if (temp.lower() == 'w'):
            temp = "Winter"
        else:
            temp = "Summer"

        query = "select id_olimpiada, nombre from Olimpiada where Olimpiada.temporada = '" + temp + "'"
        cursor1.execute(query)
        for row in cursor1.fetchall():
            print(str(row[0]) + ' - ' + row[1])
        edicion = input("Elige la edicion olimpica (id)")

        query = "select id_deporte, nombre from Deporte where exists " \
                "(select * from Evento where Deporte.id_deporte = Evento.id_deporte and id_olimpiada = " + edicion + ")"
        cursor1.execute(query)
        for row in cursor1.fetchall():
            print(str(row[0]) + ' - ' + row[1])
        deporte = input("Elige deporte (id)")

        query = "select id_evento, nombre from Evento where id_olimpiada = " + edicion + " and id_deporte = " + deporte
        cursor1.execute(query)
        for row in cursor1.fetchall():
            print(str(row[0]) + ' - ' + row[1])
        evento = input("Elige evento (id)")

        query = "select id_equipo, nombre from Equipo"
        cursor1.execute(query)
        for row in cursor1.fetchall():
            print(str(row[0]) + ' - ' + row[1])
        equipo = input("Elige equipo(id)")




        edad = input ("Introduce edad")
        medalla = input ("Introduce medalla")


        query = "insert into Participacion (id_deportista, id_evento, id_equipo, edad, medalla) values " \
                "(" + str(id) + ", " + str(evento) + ", " + str(equipo) + ", " + str(edad) + ", '" + medalla +"')"

        cursor1.execute(query)
        cursor2.execute(query)
        cn1.commit()
        cn2.commit()


        print("Participacion creada correctamente")


def eliminarParticipacion():
    cn1 = mysql.Connect(host="127.0.0.1", database="olimpiadas", user="admin", password="password")
    cn2 = sqlite3.connect('olimpiadas.db')
    cursor1 = cn1.cursor()
    cursor2 = cn2.cursor()

    nombre = input("Introduce nombre de deportista")
    query = "select * from Deportista where nombre like '%" + nombre + "%'"

    cursor1.execute(query)
    cont = 0
    for row in cursor1.fetchall():
        cont +=1
        print(str(row[0]) + " - " + row[1])
    if (cont == 0):
        print("No se ha encontrado coincidencias con ese nombre")
    else:

        deportista = input("Introduce id de deportista")

        query = "select * from Evento where exists " \
                "(select * from Participacion where Evento.id_evento = Participacion.id_evento and Participacion.id_deportista =" + deportista + ")"

        cursor1.execute(query)
        cont = 0
        for row in cursor1.fetchall():
            cont+=1
            print(str(row[0]) + " - " + row[1])

        evento = input("Introduce id de evento")


        query = "delete from Participacion  where " \
                "id_deportista = '" + deportista + "' and id_evento = '" + evento + "'"

        cursor1.execute(query)
        cursor2.execute(query)
        cn1.commit()
        cn2.commit()
        print("Participacion borrada correctamente")

        if (cont == 1):
            query = "delete from Deportista where " \
                    "id_deportista = " + deportista
            cursor1.execute(query)
            cursor2.execute(query)
            cn1.commit()
            cn2.commit()
            print("Deportista borrado correctamente")




tic= time.perf_counter()
# cargarMySQL()
# deportistaEnDeportes()

# mostrarParticipantes()
# modMedalla()

# aniadirDeportistaParticipacion()

eliminarParticipacion()
toc = time.perf_counter()
print(f"Build finished in {(toc - tic)/60:0.0f} minutes {(toc - tic)%60:0.0f} seconds")
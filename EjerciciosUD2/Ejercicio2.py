import csv

resp = input('¿Que desea hacer? \n\t1. Generar fichero csv de Olimpiadas\n\t2. Buscar deportista\n\t3. Buscar deportistas por deporte y olimpiada\n\t4. Añadir deportista\n\n\t5. Salir\n')


while resp != '5':
    if resp == '1':
        # 1

        with open('olimpiadas.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            arrGuardado = []
            with open('athlete_events.csv') as csv_file2:
                reader = csv.reader(csv_file2, delimiter=',')
                primero = True
                for linea in reader:
                    if primero:
                        cabecera = [linea[8], linea[9], linea[10], linea[11]]
                        writer.writerow(cabecera)
                        primero = False
                    else:
                        info = [linea[8], linea[9], linea[10], linea[11]]
                        if info not in arrGuardado:
                            writer.writerow(info)
                            arrGuardado.append(info)
            print("Olimpiadas.csv creado correctamente")

    elif resp =='2':
        # 2

        busqueda = input("Introduzca un deportista para iniciar la busqueda\n")
        diccionario = {}
        with open('C:/Users/Ander/Downloads/athlete_events.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            primero = True
            for linea in reader:
                if primero:
                    primero = False
                else:
                    nombre = linea[1]
                    if busqueda in nombre:
                        nombre = linea[0] + ": " + linea[1]
                        participaciones = [linea[8], linea[11], linea[13]]

                        arrClaves = diccionario.keys();
                        if nombre not in arrClaves:
                            arrParticipaciones = []
                        else:
                            arrParticipaciones = diccionario.get(nombre)

                        arrParticipaciones.append(participaciones)
                        diccionario[nombre] = arrParticipaciones

        if len(diccionario) == 0:
            print("No se han encontrado datos relacionados con ese deportista")
        else:
            arrClaves = diccionario.keys()
            for clave in arrClaves:
                print("Participaciones de " + clave)
                arrParticipaciones = diccionario.get(clave)
                for participacion in arrParticipaciones:
                    print(participacion)


    elif resp =='3':
        # 3

        deporte = input("Introduzca un deporte\n")
        anio = input("Introduzca un año\n")
        temporada = input("Introduzca una temporada\n")

        while temporada != "summer" and temporada != "winter":
            temporada = input("Temporada no existente, introuzcala de nuevo\n")

        encabezado = ""
        arrLineas = []

        with open('C:/Users/Ander/Downloads/athlete_events.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            primero = True
            for linea in reader:
                if primero:
                    primero = False
                else:
                    if deporte in linea[12].lower() and linea[9] == anio and linea[10].lower() == temporada:
                        encabezado = linea[8], linea[11], linea[12]
                        medalla = linea[14]

                        datos = [linea[1], linea[13], medalla]
                        arrLineas.append(datos)

        if len(arrLineas) == 0:
            print("No se han encontrado datos relacionados con su busqueda")
        else:
            print(encabezado)
            for linea in arrLineas:
                print(linea)

    elif resp =='4':
        # 4

        print("A continuacion introducira los datos del deportista:\n")

        nombre = input('Nombre:')

        sexo = input('Sexo:')
        while sexo != 'M' and sexo != 'F':
            sexo = input("Dato no valido: Vuelve a introducirlo")

        edad = input('Edad:')
        altura = input('Altura:')
        peso = input('Peso:')
        equipo = input('Equipo:')
        noc = input('NOC:')
        juegos = input('Juegos: ')
        anio = input('Año: ')

        temporada = input('Temporada: ')
        while temporada != "summer" and temporada != "winter":
            temporada = input("Dato no valido: Vuelve a introducirlo")

        ciudad = input('Ciudad: ')
        deporte = input('Deporte: ')
        evento = input('Evento: ')
        medalla = input('Medalla: ')

        esta = False
        id = ""
        datosArchivo = []

        with open('C:/Users/Ander/Downloads/athlete_events.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for linea in reader:
                id = linea[0]

                if esta is False and linea[1].lower() == nombre.lower():
                    esta = True
                    datos = id, nombre, sexo, edad, altura, peso, equipo, noc, juegos, anio, temporada, ciudad, deporte, evento, medalla
                    datosArchivo.append(datos)
                datosArchivo.append(linea)

        if esta is False:
            datos = [str(int(id) + 1), nombre, sexo, edad, altura, peso, equipo, noc, juegos, anio, temporada, ciudad,
                     deporte, evento, medalla]
            datosArchivo.append(datos)

        with open('C:/Users/Ander/Downloads/athlete_events.csv', 'w') as csv_file:
            writer = csv.writer(csv_file)
            for linea in datosArchivo:
                writer.writerow(linea)

    else:
        print("Opcion inexistente")

    resp = input('¿Que desea hacer? \n\t1. Generar fichero csv de Olimpiadas\n\t2. Buscar deportista\n\t3. Buscar deportistas por deporte y olimpiada\n\t4. Añadir deportista\n\n\t5. Salir\n')











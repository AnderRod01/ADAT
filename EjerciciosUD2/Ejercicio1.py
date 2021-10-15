import os
import shutil



resp = input('¿Que desea hacer? \n\t1. Crear un directorio\n\t2. Listar un directorio\n\t3. Copiar un archivo\n\t4. Mover un archivo\n\t5. Eliminar un archivo/directorio \n\n\t6. Salir\n')

while resp !='6':
    if resp=='1':
        ruta = input("Introduce el nombre y la ruta del directorio: ")
        os.mkdir(ruta)


    elif resp=='2':
        ruta = input("Introduce la ruta del directorio a listar: ")
        contenido = os.listdir(ruta)

        for fichero in contenido:
            if os.path.isfile(os.path.join(ruta, fichero)):
                print("Archivo -> ", fichero)
            else:
                print("Directorio -> ", fichero)


    elif resp=='3':
        ruta = input("Introduce la ruta del directorio a copiar: ")
        rutaNueva = input("Introduce la nueva ubicacion: ")

        shutil.copy(ruta, rutaNueva)


    elif resp=='4':
        ruta = input("Introduce la ruta del directorio a mover: ")
        rutaNueva = input("Introduce la nueva ubicacion: ")

        shutil.move(ruta, rutaNueva)


    elif resp=='5':
        ruta = input("Introduce la ruta del fichero a eliminar: ")

        if os.path.isfile(os.path.join(ruta)):
            os.remove(ruta)
        else:
            try:
                os.rmdir(ruta)
            except OSError:
                print("ERROR: Directorio no vacio")


    else:
        print("Opcion inexistente")

    resp = input(
        '¿Que desea hacer? \n\t1. Crear un directorio\n\t2. Listar un directorio\n\t3. Copiar un archivo\n\t4. Mover un archivo\n\t5. Eliminar un archivo/directorio \n\n\t6. Salir\n')

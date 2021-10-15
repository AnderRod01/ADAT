lista = []

for i in range(10):
    num = int(input('Introduce un numero impar'))
    while num % 2 == 0:
        num = int(input('Introduce otro numero'))

    lista.append(num)

resp = input('¿Que desea hacer con la lista? \n\t1. Sumatorio\n\t2. Media\n\t3. Maximo\n\t4. Minimo\n\n\t0. Salir')


def sumatorio():
    global suma, i
    suma = 0
    for i in range(10):
        suma = lista[i] + suma
    return suma


def media():
    global suma
    suma = sumatorio()
    print('Media: ', suma / 10)


def Maximo():
    maximo = max(lista)
    print('Maximo: ', maximo)


def Minimo():
    minimo = min(lista)
    print('Minimo: ', minimo)


while resp!='0':
    if resp=='1':
        print('Sumatorio: ',sumatorio())
    elif resp=='2':
        media()
    elif resp=='3':
        Maximo()
    elif resp=='4':
        Minimo()
    else:
        print('Opcion inexistente')
    resp = input('¿Que desea hacer con la lista? \n\t1. Sumatorio\n\t2. Media\n\t3. Maximo\n\t4. Minimo\n\n\t0. Salir')


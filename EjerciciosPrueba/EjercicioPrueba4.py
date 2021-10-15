lista = []

for i in range(10):
    num = int(input('Introduce un numero impar'))
    while num % 2 == 0:
        num = int(input('Introduce otro numero'))

    lista.append(num)

resp = input('¿Que desea hacer con la lista? \n\t1. Sumatorio\n\t2. Media\n\t3. Maximo\n\t4. Minimo\n\n\t0. Salir')

while resp!='0':
    if resp=='1':
        suma=0
        for i in range(10):
            suma=lista[i]+suma
        print('Sumatorio: ', suma)
    elif resp=='2':
        suma = 0
        for i in range(10):
            suma = lista[i] + suma
        print('Media: ', suma/10)
    elif resp=='3':
        maximo= max(lista)
        print ('Maximo: ', maximo)
    elif resp=='4':
        minimo= min(lista)
        print('Minimo: ', minimo)
    else:
        print('Opcion inexistente')
    resp = input('¿Que desea hacer con la lista? \n\t1. Sumatorio\n\t2. Media\n\t3. Maximo\n\t4. Minimo\n\n\t0. Salir')


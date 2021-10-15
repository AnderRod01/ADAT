lista = []
suma = 0
for i in range(10):
    num = int(input('Introduce un numero impar'))
    while num % 2 == 0:
        num = int(input('Introduce otro numero'))

    lista.append(num)
    suma = num + suma

print (lista , '\nSumatorio: ', suma , '\nMedia: ',suma/10)

lista = []
suma = 0
for i in range(10):
    num = int(input('Introduce un numero'))
    lista.append(num)
    suma = num + suma

print (lista , '\nSumatorio: ', suma , '\nMedia: ',suma/10)

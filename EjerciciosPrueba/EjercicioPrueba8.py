from EjercicioPrueba7 import Persona

p1 = Persona ('Ander', 17, 'H', 52, 163)
p2 = Persona ('Airam', 28, 'H', 80, 180)
p3 = Persona ('Elena', 19, 'M', 100, 160)




if p1.calcularIMC()==-1:
    print (p1.getNombre(), ' esta por debajo de su peso ideal')
elif p1.calcularIMC()==0:
    print (p1.getNombre(), ' esta en su peso ideal')
else:
    print(p1.getNombre(), ' tiene sobrepeso')

if p2.calcularIMC()==-1:
    print (p2.getNombre(), ' esta por debajo de su peso ideal')
elif p2.calcularIMC()==0:
    print (p2.getNombre(), ' esta en su peso ideal')
else:
    print(p2.getNombre(), ' tiene sobrepeso')

if p3.calcularIMC()==-1:
    print (p3.getNombre(), ' esta por debajo de su peso ideal')
elif p3.calcularIMC()==0:
    print (p3.getNombre(), ' esta en su peso ideal')
else:
    print(p3.getNombre(), ' tiene sobrepeso')

if p1.esMayorDeEdad():
    print(p1.getNombre(), ' es mayor de edad')
else:
    print(p1.getNombre(), ' es menor de edad')




if p2.esMayorDeEdad():
    print(p2.getNombre(), ' es mayor de edad')
else:
    print(p2.getNombre(), ' es menor de edad')

if p3.esMayorDeEdad():
    print(p3.getNombre(), ' es mayor de edad')
else:
    print(p3.getNombre(), ' es menor de edad')




print(p1.toString())
print(p2.toString())
print(p3.toString())


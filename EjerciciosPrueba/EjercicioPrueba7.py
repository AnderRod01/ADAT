import random


class Persona:
    MINIMO_IMC = 20
    MAXIMO_IMC = 25

    def __init__(self, nombre='', edad=0, sexo='H', peso=0, altura=0):
        self.__nombre=nombre
        self.__edad=edad
        self.__dni=self.__generaDNI()
        self.__sexo=sexo
        self.__peso=peso
        self.__altura=altura

    def setAltura(self, altura):
        self.altura = altura

    def setPeso(self, peso):
        self.peso = peso

    def setSexo(self, sexo):
        self.sexo = sexo

    def setEdad(self, edad):
        self.edad = edad

    def setNombre(self, nombre):
        self.nombre = nombre


    def getAltura(self):
        return self.__altura

    def getPeso(self):
        return self.__peso

    def getSexo(self):
        return self.__sexo

    def getEdad(self):
        return self.__edad

    def getNombre(self):
        return self.__nombre

    def getDni (self):
        return self.__dni



    def calcularIMC(self):
        MINIMO_IMC=20
        MAXIMO_IMC=25

        try:
            imc = self.getPeso() / (self.getAltura() / 100) ** 2

            if imc<MINIMO_IMC:
                return -1
            elif imc<MAXIMO_IMC:
                return 0
            else:
                return 1
        except:
            print ('Datos no validos')
            return None

    def esMayorDeEdad(self):
        if self.getEdad()>=18:
            return True
        else:
            return False

    def toString(self):
        return 'Nombre: ', self.getNombre(), '   Edad: ', self.getEdad(), '  DNI: ', self.getDni(), 'Sexo: ',self.getSexo(), '  Peso: ', self.getPeso(), '   Altura: ', self.getAltura()


    def __generaDNI(self):
        nDni=random.randint(10000000, 99999999)
        palabra = 'TRWAGMYFPDXBNJZSQVHLCKE'
        return repr(nDni) + '' + palabra[nDni % 23]
class Criptografo:

    def encriptar(txt):
        nuevoTxt= ''
        for caracter in txt:
            ascii=ord(caracter)
            ascii= ascii+1
            nuevoTxt= nuevoTxt + chr(ascii)

        return nuevoTxt

    def desencriptar(txt):
        nuevoTxt= ''
        for caracter in txt:
            ascii=ord(caracter)
            ascii= ascii-1
            nuevoTxt= nuevoTxt + chr(ascii)

        return nuevoTxt

print(Criptografo.encriptar('Hola'))
print(Criptografo.desencriptar('ipmb'))
import pandas as pd
import csv, operator

df_olimpiadas = pd.read_csv("/home/dm2/Descargas/athlete_events.csv")

#1
'''
df=df_olimpiadas[['Year', 'Games', 'Season', 'City']].drop_duplicates()
df.to_csv('Olimpiadas.csv', index=False)
'''


#2
'''
busqueda = input ("Introduzca el nombre de un deportista")

print(df_olimpiadas[df_olimpiadas.Name == busqueda][['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Games', 'Event']])

'''

#3

deporte ="Speed Skating" #input ("Introduzca un deporte")
anio ="1988" #input ("Introduzca un año")
season ="Winter" #input ("Introduzca una temporada")

juegos = df_olimpiadas[(df_olimpiadas.Games ==anio+ " "+  season) & (df_olimpiadas.Sport == deporte)]

print (juegos[['City', 'Games', 'Sport']].drop_duplicates())

print (juegos [['Name', 'Event', 'Medal']])


#4
'''"ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"'''
'''
id= df_olimpiadas['ID'].tail(1) +1

nombre=input('Nombre:')
sexo= input('Sexo:')
edad= input('Edad:')
altura= input ('Altura:')
peso=input ('Peso:')
equipo= input('Equipo:')
noc= input('NOC:')
juegos= input ('Juegos: ')
anio = input('Año: ')
temporada = input ('Temporada: ')
ciudad = input ('Ciudad: ')
deporte = input ('Deporte: ')
evento = input ('Evento: ')
medalla = input ('Medalla: ')

fila= [(id, nombre,sexo, edad, altura,peso,equipo,noc, juegos, anio, temporada, ciudad, deporte, evento, medalla)]
dfNuevo = pd.DataFrame(fila , columns=["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"])
df_olimpiadas.append(dfNuevo, ignore_index=True)


print( df_olimpiadas.tail())
'''
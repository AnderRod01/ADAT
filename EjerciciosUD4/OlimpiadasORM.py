from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


class Olimpiada(Base):
    __tablename__ = 'Olimpiada'
    id_olimpiada = Column(Integer, primary_key=True)
    nombre = Column(String)
    anio = Column(Integer)
    temporada = Column(String)
    ciudad = Column(String)


class Deportista(Base):
    __tablename__ = 'Deportista'
    id_deportista = Column(Integer, primary_key=True)
    nombre = Column(String)
    sexo = Column(String)
    peso = Column(Integer)
    altura = Column(Integer)


class Deporte(Base):
    __tablename__ = 'Deporte'
    id_deporte = Column(Integer, primary_key=True)
    nombre = Column(String)


class Equipo(Base):
    __tablename__ = 'Equipo'
    id_equipo = Column(Integer, primary_key=True)
    nombre = Column(String)
    iniciales = Column(String)


class Evento(Base):
    __tablename__ = 'Evento'
    id_evento = Column(Integer, primary_key=True)
    nombre = Column(String)
    id_olimpiada = Column(Integer, ForeignKey('Olimpiada.id_olimpiada'))
    id_deporte = Column(Integer, ForeignKey('Deporte.id_deporte'))
    olimpiada = relationship("Olimpiada", back_populates="eventos")
    deporte = relationship("Deporte", back_populates="eventos")


class Participacion(Base):
    __tablename__ = 'Participacion'
    id_deportista = Column(Integer, ForeignKey('Deportista.id_deportista'), primary_key=True)
    id_evento = Column(Integer, ForeignKey('Evento.id_evento'), primary_key=True)
    id_equipo = Column(Integer, ForeignKey('Equipo.id_equipo'))
    edad = Column(Integer)
    medalla = Column(String)
    deportista = relationship("Deportista", back_populates="participaciones")
    evento = relationship("Evento", back_populates="participaciones")
    equipo = relationship("Equipo", back_populates="participaciones")


Olimpiada.eventos = relationship("Evento", order_by=Evento.id_evento, back_populates="olimpiada")
Deporte.eventos = relationship("Evento", order_by=Evento.id_evento, back_populates="deporte")

Deportista.participaciones = relationship("Participacion", back_populates="deportista")
Evento.participaciones = relationship("Participacion", back_populates="evento")
Equipo.participaciones = relationship("Participacion", back_populates="equipo")


def mostrarParticipantes():
    bbdd = input("MySQL o SQLite?")

    if bbdd.lower() == "mysql":
        engine = create_engine('mysql+pymysql://admin:password@localhost/olimpiadas')
    else:
        engine = create_engine('sqlite:///olimpiadas.db')

    cn = engine.connect()
    Session = sessionmaker(bind=engine)
    session = Session()

    temp = input("Winter o Summer? (W/S)")
    while temp.lower() != 'w' and temp.lower() != 's':
        temp = input("Debes introducir W o S")

    if temp.lower() == 'w':
        temp = "Winter"
    else:
        temp = "Summer"

    result = session.query(Olimpiada).filter(Olimpiada.temporada == temp)


    olimpiadas = {}
    for row in result:
        print("\t" + str(row.id_olimpiada) + " - " + row.nombre)
        olimpiadas [row.id_olimpiada] = row


    edicion = int(input("Elige la edicion olimpica (id)"))


    deportesDif = {}
    for evento in olimpiadas[edicion].eventos:
        if not evento.deporte.id_deporte in deportesDif:
            deportesDif[evento.deporte.id_deporte] = evento.deporte



    for row in deportesDif.values():
        print("\t" +str(row.id_deporte) + " - " + row.nombre)

    deporte = int(input("Elige el deporte (id)"))

    eventos = {}
    for evento in olimpiadas[edicion].eventos:
        if evento.deporte.id_deporte == deportesDif[deporte].id_deporte:
            print("\t" + str(evento.id_evento) + " - " + evento.nombre)
            eventos[evento.id_evento] = evento


    evento = int(input("Elige evento (id)"))

    print("=" * 50)
    print(olimpiadas[edicion].temporada + '\t' + olimpiadas[edicion].nombre + '\t' + deportesDif[deporte].nombre + '\t' + eventos[evento].nombre)
    print("=" * 50)

    for part in eventos[evento].participaciones:
        print(
            part.deportista.nombre + ' - ' + str(part.deportista.altura) + ' - ' + str(part.deportista.peso) + ' - ' + str(part.edad) + ' - ' + part.evento.nombre + ' - ' + part.medalla)



def modificarMedalla():
    engine1 = create_engine('mysql+pymysql://admin:password@localhost/olimpiadas')
    engine2 = create_engine('sqlite:///olimpiadas.db')

    cn1 = engine1.connect()
    Session = sessionmaker(bind=engine1)
    session1 = Session()

    cn2 = engine2.connect()
    Session = sessionmaker(bind=engine2)
    session2 = Session()


    nombre = input ("Introduce nombre de deportista")

    result = session1.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))

    deportistas = {}
    for row in result:
        print("\t" +str(row.id_deportista) + " - " + row.nombre)
        deportistas[row.id_deportista] = row

    deportista = int(input("Elige deportista (id)"))


    partsDeDeportista = session1.query(Participacion).filter(Participacion.id_deportista == deportista)

    eventos = {}
    for part in partsDeDeportista:
        print("\t" + str(part.evento.id_evento) + " - " + part.evento.nombre)
        eventos[part.evento.id_evento] = part.evento

    evento = int(input("Elige evento(id)"))

    medalla = input("Introduce nuevo valor para medalla (Gold, Silver,Bronze,NA)")
    while (medalla.lower() != 'gold' and medalla.lower() != 'silver' and medalla.lower() != 'bronze' and medalla.lower() != 'na'):
        medalla = input("Debes introducir Gold, Silver, Bronze o NA")

    session1.query(Participacion).filter(
        Participacion.id_deportista == deportista and Participacion.id_evento==evento).update({Participacion.medalla:medalla}, synchronize_session = False)

    session2.query(Participacion).get((deportista, evento)).medalla = medalla

    session1.commit()
    session2.commit()


def aniadirDeportista():
    engine1 = create_engine('mysql+pymysql://admin:password@localhost/olimpiadas')
    engine2 = create_engine('sqlite:///olimpiadas.db')

    cn1 = engine1.connect()
    Session = sessionmaker(bind=engine1)
    session1 = Session()

    cn2 = engine2.connect()
    Session = sessionmaker(bind=engine2)
    session2 = Session()

    nombre = input("Introduce nombre de deportista")

    result = session1.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))

    listaDeportistas = []

    for row in result:
        listaDeportistas.append(row.id_deportista)
        print("\t" +str(row.id_deportista) + " - " + row.nombre)

    if len(listaDeportistas)==0:

        print("El deportista no existe. Inserte los datos correspontientes para crearlo:\n")

        sexo = input("Introduce sexo del deportista")
        while (sexo.lower() != 'm' and sexo.lower() != 'f'):
            sexo = input("Debes introducir M o F")

        peso = input("Introduce peso del deportista")
        altura = input("Introduce altura del deportista")

        if (peso == 0):
            peso = None
        if (altura == 0):
            altura = None

        deportista = session1.query(Deportista).order_by(desc(Deportista.id_deportista)).first().id_deportista +1


        nuevoDeportista = Deportista(id_deportista=deportista, nombre=nombre, sexo=sexo, peso=peso, altura=altura)
        nDepSQLITE = Deportista(id_deportista=deportista, nombre=nombre, sexo=sexo, peso=peso, altura=altura)
        session1.add(nuevoDeportista)
        session1.commit()

        session2.add(nDepSQLITE)
        session2.commit()

    else:
        deportista = int(input("selecciona deportista (id)"))

    temp = input("Winter o Summer? (W/S)")
    while temp.lower() != 'w' and temp.lower() != 's':
        temp = input("Debes introducir W o S")

    if temp.lower() == 'w':
        temp = "Winter"
    else:
        temp = "Summer"

    result = session1.query(Olimpiada).filter(Olimpiada.temporada == temp)

    olimpiadas = {}
    for row in result:
        print("\t" + str(row.id_olimpiada) + " - " + row.nombre)
        olimpiadas[row.id_olimpiada] = row

    edicion = int(input("Elige la edicion olimpica (id)"))

    deportesDif = {}
    for evento in olimpiadas[edicion].eventos:
        if not evento.deporte.id_deporte in deportesDif:
            deportesDif[evento.deporte.id_deporte] = evento.deporte

    for row in deportesDif.values():
        print("\t" + str(row.id_deporte) + " - " + row.nombre)

    deporte = int(input("Elige el deporte (id)"))

    eventos = {}
    for evento in olimpiadas[edicion].eventos:
        if evento.deporte.id_deporte == deportesDif[deporte].id_deporte:
            print("\t" + str(evento.id_evento) + " - " + evento.nombre)
            eventos[evento.id_evento] = evento

    evento = int(input("Elige evento (id)"))

    listaEquipos = []
    result = session1.query(Equipo).all()
    for row in result:
        listaEquipos.append(row.id_equipo)
        print("\t" + str(row.id_equipo) + " - " + row.nombre)
    equipo = int(input("Elige equipo (id)"))

    nuevaParticipacion = Participacion(id_deportista=deportista, id_evento=evento, id_equipo=equipo, edad=None,
                                       medalla=None)

    session1.add(nuevaParticipacion)
    session1.commit()

    session2.add(nuevaParticipacion)
    session2.commit()

def borrarParticipacion():
        engine1 = create_engine('mysql+pymysql://admin:password@localhost/olimpiadas')
        engine2 = create_engine('sqlite:///olimpiadas.db')

        cn1 = engine1.connect()
        Session = sessionmaker(bind=engine1)
        session1 = Session()

        cn2 = engine2.connect()
        Session = sessionmaker(bind=engine2)
        session2 = Session()

        nombre = input("Introduce nombre de deportista")

        result = session1.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))

        listaDeportistas = {}

        for row in result:
            listaDeportistas[row.id_deportista] = row.participaciones
            print("\t" + str(row.id_deportista) + " - " + row.nombre)

        while(len(listaDeportistas) == 0):
            nombre = input("Deportista no existente. Introduce otro nombre")
            result = session1.query(Deportista).filter(Deportista.nombre.like("%" + nombre + "%"))
            for row in result:
                listaDeportistas.append(row.id_deportista)
                print("\t" + str(row.id_deportista) + " - " + row.nombre)

        deportista = int(input("selecciona deportista (id)"))

        listaParticipaciones=[]
        for participacion in listaDeportistas[deportista]:
            print (str(participacion.id_evento) + " - " + session1.query(Evento).get(participacion.id_evento).nombre)
            listaParticipaciones.append(participacion.id_evento)
        evento = int(input ("selecciona evento (id)"))

        session1.query(Participacion).filter(Participacion.id_deportista == deportista,
                                             Participacion.id_evento == evento).delete()
        session1.commit()

        session2.query(Participacion).filter(Participacion.id_deportista == deportista,
                                             Participacion.id_evento == evento).delete
        session2.commit()

        print("Participacion borrada")

        result = session1.query(Participacion).filter(Participacion.id_deportista==deportista).count()
        if result== 0:
            session1.query(Deportista).filter(Deportista.id_deportista == deportista).delete()
            session1.commit()

            session2.query(Deportista).filter(Deportista.id_deportista == deportista).delete()
            session2.commit()
            print("deportista borrado")


# menu
resp = int(input('¿Que desea hacer?'
             '\n\t1. Listado de deportistas participantes'
             '\n\t2. Modificar medalla deportista'
             '\n\t3. Añadir deportista/participación'
             '\n\t4. Eliminar participación\n\n\t'
             '0. Salir\n'))

while resp != 0:
    print()
    if resp == 1:
        mostrarParticipantes()
    elif resp == 2:
        modificarMedalla()
    elif resp == 3:
        aniadirDeportista()
    elif resp == 4:
        borrarParticipacion()
    else:
        print("No existe esa opcion")

    resp = int(input('¿Que desea hacer?'
                     '\n\t1. Listado de deportistas participantes'
                     '\n\t2. Modificar medalla deportista'
                     '\n\t3. Añadir deportista/participación'
                     '\n\t4. Eliminar participación\n\n\t'
                     '0. Salir\n'))




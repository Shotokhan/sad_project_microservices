from utenteDAO import UtenteDAO
from projectUtils import hash_pw
import datetime
from appExceptions import RowNotFoundException


class Utente:
    def __init__(self, _id, nome="", cognome="", dataNascita=datetime.date(2000, 1, 1), luogoNascita="",
                 email="", telefono="", password=""):
        self.id = _id
        self.nome = nome
        self.cognome = cognome
        self.dataNascita = dataNascita
        self.luogoNascita = luogoNascita
        self.email = email
        self.telefono = telefono
        self.password = hash_pw(password)

    def addUtente(self, db):
        utente = UtenteDAO(nome=self.nome, cognome=self.cognome, dataNascita=self.dataNascita,
                           luogoNascita=self.luogoNascita, email=self.email, telefono=self.telefono,
                           password=self.password)
        db.session.add(utente)
        db.session.commit()
        db.session.refresh(utente)
        self.id = utente.id
        return utente

    def getUtenteByID(self, db, delete=False):
        _id = self.id
        utente = db.session.query(UtenteDAO).filter(UtenteDAO.id == _id).first()
        if utente is None:
            raise RowNotFoundException("Row not found in 'utente' table when searching by ID: {}".format(_id))
        if delete:
            db.session.delete(utente)   # acts like "pop user"
            db.session.commit()
        self.nome = utente.nome
        self.cognome = utente.cognome
        self.dataNascita = utente.dataNascita
        self.luogoNascita = utente.luogoNascita
        self.email = utente.email
        self.telefono = utente.telefono
        self.password = utente.password
        return utente

    def __eq__(self, other):
        # assuming a refreshed object
        if isinstance(other, Utente):
            cmp = True
            cmp &= self.id == other.id
            cmp &= self.nome == other.nome
            cmp &= self.cognome == other.cognome
            cmp &= self.dataNascita == other.dataNascita
            cmp &= self.luogoNascita == other.luogoNascita
            cmp &= self.email == other.email
            cmp &= self.telefono == other.telefono
            cmp &= self.password == other.password
            return cmp
        else:
            return False

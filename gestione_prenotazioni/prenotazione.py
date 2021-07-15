from prenotazioneDAO import PrenotazioneDAO
from appExceptions import RowNotFoundException, AlreadyExistException
import datetime
from sqlalchemy.exc import IntegrityError


class Prenotazione:
    def __init__(self, _id=0, idPaziente=0, luogoVaccino="", dataVaccino=datetime.date(2000, 1, 1),
                 codiceFiscale="", tesseraSanitaria="", luogoResidenza="", nome="", cognome="",
                 email="", telefono=""):
        self.id = _id
        self.idPaziente = idPaziente
        self.luogoVaccino = luogoVaccino
        self.dataVaccino = dataVaccino
        self.codiceFiscale = codiceFiscale
        self.tesseraSanitaria = tesseraSanitaria
        self.luogoResidenza = luogoResidenza
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.telefono = telefono

    def creaNuovaPrenotazione(self, db, deltaDays=3, maxBookingsPerDay=5):
        listaPrenotazioni = Prenotazione.getAllPrenotazioniFuture(db)
        datesCount = {p.dataVaccino: 0 for p in listaPrenotazioni}
        for p in listaPrenotazioni:
            datesCount[p.dataVaccino] += 1
        # new booking starting from 'deltaDays' days from now
        delta = datetime.timedelta(days=deltaDays)
        dataVaccino = datetime.date.today() + delta
        while dataVaccino in datesCount and datesCount[dataVaccino] >= maxBookingsPerDay:
            deltaDays += 1
            delta = datetime.timedelta(days=deltaDays)
            dataVaccino = datetime.date.today() + delta
        self.dataVaccino = dataVaccino
        self.luogoVaccino = self.luogoResidenza     # stub
        return self.addPrenotazione(db)

    def addPrenotazione(self, db):
        prenotazione = PrenotazioneDAO(idPaziente=self.idPaziente, luogoVaccino=self.luogoVaccino,
                                       dataVaccino=self.dataVaccino, codiceFiscale=self.codiceFiscale,
                                       tesseraSanitaria=self.tesseraSanitaria, luogoResidenza=self.luogoResidenza,
                                       nome=self.nome, cognome=self.cognome, email=self.email, telefono=self.telefono)
        db.session.add(prenotazione)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise AlreadyExistException("Tried to add a 'prenotazione' for a 'paziente' who already added one.")
        db.session.refresh(prenotazione)
        self.id = prenotazione.id
        return prenotazione

    def getPrenotazioneByID(self, db, delete=False):
        _id = self.id
        prenotazione = db.session.query(PrenotazioneDAO).filter(PrenotazioneDAO.id == _id).first()
        if prenotazione is None:
            raise RowNotFoundException("Row not found in 'prenotazione' table when searching by ID: {}".format(_id))
        if delete:
            db.session.delete(prenotazione)   # acts like "pop prenotazione"
            db.session.commit()
        Prenotazione.mapObject(self, prenotazione)
        return prenotazione

    def getPrenotazioneByCodiceFiscale(self, db):
        # precondition: create a Prenotazione object setting codiceFiscale
        prenotazione = db.session.query(PrenotazioneDAO).filter(
            PrenotazioneDAO.codiceFiscale == self.codiceFiscale).first()
        if prenotazione is None:
            raise RowNotFoundException("Row not found in 'prenotazione' table when searching by codiceFiscale: {}"
                                       .format(self.codiceFiscale))
        Prenotazione.mapObject(self, prenotazione)
        return prenotazione

    @staticmethod
    def getAllPrenotazioniFuture(db):
        # default: ascending order
        prenotazioni = db.session.query(PrenotazioneDAO).filter(
            PrenotazioneDAO.dataVaccino >= datetime.date.today()
        ).order_by(PrenotazioneDAO.dataVaccino).all()
        listaPrenotazioni = []
        for pDAO in prenotazioni:
            prenotazione = Prenotazione()
            Prenotazione.mapObject(prenotazione, pDAO)
            listaPrenotazioni.append(prenotazione)
        return listaPrenotazioni

    @staticmethod
    def mapObject(prenotazione, prenotazioneDAO):
        prenotazione.id = prenotazioneDAO.id
        prenotazione.idPaziente = prenotazioneDAO.idPaziente
        prenotazione.luogoVaccino = prenotazioneDAO.luogoVaccino
        prenotazione.dataVaccino = prenotazioneDAO.dataVaccino
        prenotazione.codiceFiscale = prenotazioneDAO.codiceFiscale
        prenotazione.tesseraSanitaria = prenotazioneDAO.tesseraSanitaria
        prenotazione.luogoResidenza = prenotazioneDAO.luogoResidenza
        prenotazione.nome = prenotazioneDAO.nome
        prenotazione.cognome = prenotazioneDAO.cognome
        prenotazione.email = prenotazioneDAO.email
        prenotazione.telefono = prenotazioneDAO.telefono

    def __eq__(self, other):
        if isinstance(other, Prenotazione):
            cmp = True
            cmp &= self.id == other.id
            cmp &= self.idPaziente == other.idPaziente
            cmp &= self.luogoVaccino == other.luogoVaccino
            cmp &= self.dataVaccino == other.dataVaccino
            cmp &= self.codiceFiscale == other.codiceFiscale
            cmp &= self.tesseraSanitaria == other.tesseraSanitaria
            cmp &= self.luogoResidenza == other.luogoResidenza
            cmp &= self.nome == other.nome
            cmp &= self.cognome == other.cognome
            cmp &= self.email == other.email
            cmp &= self.telefono == other.telefono
            return cmp
        else:
            return False

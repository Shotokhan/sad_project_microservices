from utente import Utente
from pazienteDAO import PazienteDAO
from utenteDAO import UtenteDAO
from appExceptions import RowNotFoundException, AlreadyExistException
import datetime
from sqlalchemy.exc import IntegrityError


class Paziente(Utente):
    def __init__(self, idPaziente=0, idUtente=0, nome="", cognome="", dataNascita=datetime.date(2000, 1, 1),
                 luogoNascita="", email="", telefono="", password="", codiceFiscale="",
                 tesseraSanitaria="", luogoResidenza=""):
        super().__init__(idUtente, nome, cognome, dataNascita, luogoNascita, email, telefono, password)
        self.codiceFiscale = codiceFiscale
        self.tesseraSanitaria = tesseraSanitaria
        self.luogoResidenza = luogoResidenza
        self.idPaziente = idPaziente

    def addPaziente(self, db):
        utente = self.addUtente(db)
        paziente = PazienteDAO(codiceFiscale=self.codiceFiscale, tesseraSanitaria=self.tesseraSanitaria,
                               luogoResidenza=self.luogoResidenza, utente=utente)
        db.session.add(paziente)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            utente = Utente(utente.id)
            utente.getUtenteByID(db, delete=True)
            raise AlreadyExistException("Tried to add a 'paziente' with codiceFiscale and/or tesseraSanitaria"
                                        "equal to another existing 'paziente'")
        db.session.refresh(paziente)
        self.id = utente.id
        self.idPaziente = paziente.id
        return paziente

    def getPazienteByID(self, db, delete=False):
        _id = self.idPaziente
        utenteId = self.id
        # I use the join to check for existence, then I make other queries for code re-use
        paziente = db.session.query(PazienteDAO).join(UtenteDAO). \
            filter(utenteId == UtenteDAO.id).filter(_id == PazienteDAO.id).first()
        if paziente is None:
            raise RowNotFoundException("Row not found in 'paziente' table when searching by ID: {}, "
                                       "and joining 'utente' on ID: ".format(_id, utenteId))

        self.getUtenteByID(db, delete=delete)
        if delete:
            db.session.delete(paziente)
            db.session.commit()
        self.codiceFiscale = paziente.codiceFiscale
        self.tesseraSanitaria = paziente.tesseraSanitaria
        self.luogoResidenza = paziente.luogoResidenza
        return paziente

    def authPaziente(self, db):
        # Precondition: you have to create a Paziente object setting only codiceFiscale and password
        # password is automatically hashed when you create the object
        # this time I make a true join, with all fields
        paziente = db.session.query(PazienteDAO, UtenteDAO).filter(
                    PazienteDAO.utenteId == UtenteDAO.id).filter(
                    PazienteDAO.codiceFiscale == self.codiceFiscale).filter(
                    UtenteDAO.password == self.password).first()
        if paziente is None:
            raise RowNotFoundException(
                "Row not found in 'paziente' table when searching by CF: {}, "
                "password hash: {} and joining 'utente' on feasible IDs".format(self.codiceFiscale, self.password)
            )
        # code re-use for filling fields
        self.id = paziente['PazienteDAO'].utenteId
        self.getUtenteByID(db)
        self.idPaziente = paziente['PazienteDAO'].id
        self.codiceFiscale = paziente['PazienteDAO'].codiceFiscale
        self.tesseraSanitaria = paziente['PazienteDAO'].tesseraSanitaria
        self.luogoResidenza = paziente['PazienteDAO'].luogoResidenza
        return paziente

    def __eq__(self, other):
        if isinstance(other, Paziente):
            cmp = True
            # call eq method of super-class
            cmp &= super(Paziente, self).__eq__(other)
            cmp &= self.codiceFiscale == other.codiceFiscale
            cmp &= self.tesseraSanitaria == other.tesseraSanitaria
            cmp &= self.luogoResidenza == other.luogoResidenza
            return cmp
        else:
            return False

from utente import Utente
from operatoreDAO import OperatoreDAO
from utenteDAO import UtenteDAO
from appExceptions import RowNotFoundException, AlreadyExistException
import datetime
from sqlalchemy.exc import IntegrityError


class Operatore(Utente):
    def __init__(self, idOperatore=0, idUtente=0, nome="", cognome="", dataNascita=datetime.date(2000, 1, 1),
                 luogoNascita="", email="", telefono="", password="", idAslOperatore=""):
        super().__init__(idUtente, nome, cognome, dataNascita, luogoNascita, email, telefono, password)
        self.idAslOperatore = idAslOperatore
        self.idOperatore = idOperatore

    def addOperatore(self, db):
        utente = self.addUtente(db)
        operatore = OperatoreDAO(idAslOperatore=self.idAslOperatore, utente=utente)
        db.session.add(operatore)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            utente = Utente(utente.id)
            utente.getUtenteByID(db, delete=True)
            raise AlreadyExistException("Tried to add a 'operatore' with idAslOperatore"
                                        "equal to another existing 'operatore'")
        db.session.refresh(operatore)
        self.id = utente.id
        self.idOperatore = operatore.id
        return operatore

    def getOperatoreByID(self, db, delete=False):
        _id = self.idOperatore
        utenteId = self.id
        # I use the join to check for existence, then I make other queries for code re-use
        operatore = db.session.query(OperatoreDAO).join(UtenteDAO). \
            filter(utenteId == UtenteDAO.id).filter(_id == OperatoreDAO.id).first()
        if operatore is None:
            raise RowNotFoundException("Row not found in 'operatore' table when searching by ID: {}, "
                                       "and joining 'utente' on ID: ".format(_id, utenteId))

        self.getUtenteByID(db, delete=delete)
        if delete:
            db.session.delete(operatore)
            db.session.commit()
        self.idAslOperatore = operatore.idAslOperatore
        return operatore

    def authOperatore(self, db):
        # Precondition: you have to create a Paziente object setting only codiceFiscale and password
        # password is automatically hashed when you create the object
        # this time I make a true join, with all fields
        operatore = db.session.query(OperatoreDAO, UtenteDAO).filter(
                    OperatoreDAO.utenteId == UtenteDAO.id).filter(
                    OperatoreDAO.idAslOperatore == self.idAslOperatore).filter(
                    UtenteDAO.password == self.password).first()
        if operatore is None:
            raise RowNotFoundException(
                "Row not found in 'operatore' table when searching by ASL id: {}, "
                "password hash: {} and joining 'utente' on feasible IDs".format(self.idAslOperatore, self.password)
            )
        # code re-use for filling fields
        self.id = operatore['OperatoreDAO'].utenteId
        self.getUtenteByID(db)
        self.idOperatore = operatore['OperatoreDAO'].id
        self.idAslOperatore = operatore['OperatoreDAO'].idAslOperatore
        return operatore

    def __eq__(self, other):
        if isinstance(other, Operatore):
            cmp = True
            # call eq method of super-class
            cmp &= super(Operatore, self).__eq__(other)
            cmp &= self.idAslOperatore == other.idAslOperatore
            return cmp
        else:
            return False

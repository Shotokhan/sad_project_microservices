from app_singleton import App
from utenteDAO import UtenteDAO


db = App().db


class PazienteDAO(db.Model):
    __tablename__ = 'paziente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codiceFiscale = db.Column(db.String, nullable=False, unique=True)
    tesseraSanitaria = db.Column(db.String, nullable=False, unique=True)
    luogoResidenza = db.Column(db.String, nullable=False)
    utenteId = db.Column(db.Integer, db.ForeignKey(UtenteDAO.id), nullable=False, unique=True)
    utente = db.relationship(UtenteDAO)  # to restore the entire object with a Join


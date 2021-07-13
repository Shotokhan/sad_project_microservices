from app_singleton import App
from utenteDAO import UtenteDAO


db = App().db


class OperatoreDAO(db.Model):
    __tablename__ = 'operatore'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idAslOperatore = db.Column(db.String, nullable=False, unique=True)
    utenteId = db.Column(db.Integer, db.ForeignKey(UtenteDAO.id), nullable=False, unique=True)
    utente = db.relationship(UtenteDAO)  # to restore the entire object with a Join

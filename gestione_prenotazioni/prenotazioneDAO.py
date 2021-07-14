from app_singleton import App

db = App().db


class PrenotazioneDAO(db.Model):
    __tablename__ = 'prenotazione'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idPaziente = db.Column(db.Integer, nullable=False, unique=True)
    luogoVaccino = db.Column(db.String, nullable=False)
    dataVaccino = db.Column(db.Date, nullable=False)
    codiceFiscale = db.Column(db.String, nullable=False, unique=True)
    tesseraSanitaria = db.Column(db.String, nullable=False, unique=True)
    luogoResidenza = db.Column(db.String, nullable=False)
    nome = db.Column(db.String, nullable=False)
    cognome = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    telefono = db.Column(db.String, nullable=False)

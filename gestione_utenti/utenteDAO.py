from app_singleton import App

db = App().db


class UtenteDAO(db.Model):
    __tablename__ = 'utente'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String, nullable=False)
    cognome = db.Column(db.String, nullable=False)
    dataNascita = db.Column(db.Date, nullable=False)
    luogoNascita = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    telefono = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

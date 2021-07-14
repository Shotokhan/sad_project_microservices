import sys
import datetime

sys.path.insert(0, "..")
from app_singleton import App

# in-memory database
manager = App(__name__, config={'db': "sqlite://", 'secret': '', 'session_validity_days': 1})

# need this import for db.create_all()
from utenteDAO import UtenteDAO
from utente import Utente
from appExceptions import RowNotFoundException

manager.db.create_all()


def test_insert_and_get():
    user = Utente(0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                  "password")
    user.addUtente(manager.db)
    user_from_db = Utente(user.id)
    try:
        user_from_db.getUtenteByID(manager.db)
    except RowNotFoundException:
        assert False, "The user should be found in the DB"
    assert user == user_from_db, "Should be the same user"
    try:
        user.getUtenteByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_multiple_ins_and_get_and_compare():
    mario = Utente(0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                   "password")
    mario.addUtente(manager.db)
    claudia = Utente(0, "claudia", "verdi", datetime.date(1982, 5, 17), "roma", "cla.verdi@lol.it", "123456788",
                     "strong_password")
    claudia.addUtente(manager.db)
    mario_from_db = Utente(mario.id)
    mario_from_db.getUtenteByID(manager.db)
    claudia_from_db = Utente(claudia.id)
    claudia_from_db.getUtenteByID(manager.db)
    assert not (mario_from_db == claudia_from_db), "They should be different users"
    try:
        mario.getUtenteByID(manager.db, delete=True)
        claudia.getUtenteByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_user_not_in_db():
    user = Utente(0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                  "password")
    user.addUtente(manager.db)
    user_from_db = Utente(user.id + 1)
    ex = False
    try:
        user_from_db.getUtenteByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The user should NOT be found in the DB"
    try:
        user.getUtenteByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_get_after_delete():
    user = Utente(0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                  "password")
    user.addUtente(manager.db)
    user_from_db = Utente(user.id)
    ex = False
    try:
        user_from_db.getUtenteByID(manager.db, delete=True)
    except RowNotFoundException:
        assert False, "The user should be found in the DB before getting deleted"
    try:
        user.getUtenteByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The user should NOT be found in the DB"


tests = [test_insert_and_get, test_multiple_ins_and_get_and_compare, test_user_not_in_db, test_get_after_delete]

import sys
import datetime

sys.path.insert(0, "..")
from app_singleton import App

# in-memory database
manager = App(__name__, config={'db': "sqlite://", 'secret': '', 'session_validity_days': 1})

# need this import for db.create_all()
from utenteDAO import UtenteDAO
from pazienteDAO import PazienteDAO
from paziente import Paziente
from appExceptions import RowNotFoundException, AlreadyExistException

manager.db.create_all()


def test_insert_and_get():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                  "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user_from_db = Paziente(user.idPaziente, user.id)
    try:
        user_from_db.getPazienteByID(manager.db)
    except RowNotFoundException:
        assert False, "The user should be found in the DB"
    assert user == user_from_db, "Should be the same user"
    try:
        user.getPazienteByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_multiple_ins_and_get_and_compare():
    mario = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                   "password", "CF", "tessera", "roma")
    mario.addPaziente(manager.db)
    claudia = Paziente(0, 0, "claudia", "verdi", datetime.date(1982, 5, 17), "roma", "cla.verdi@lol.it", "123456788",
                     "strong_password", "CF2", "tessera2", "roma")
    claudia.addPaziente(manager.db)
    mario_from_db = Paziente(mario.idPaziente, mario.id)
    mario_from_db.getPazienteByID(manager.db)
    claudia_from_db = Paziente(claudia.idPaziente, claudia.id)
    claudia_from_db.getPazienteByID(manager.db)
    assert not (mario_from_db == claudia_from_db), "They should be different users"
    try:
        mario.getPazienteByID(manager.db, delete=True)
        claudia.getPazienteByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_user_not_in_db():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user_from_db = Paziente(user.idPaziente + 1, user.id)
    ex = False
    try:
        user_from_db.getPazienteByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The user should NOT be found in the DB"
    try:
        user.getPazienteByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_get_after_delete():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                    "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user_from_db = Paziente(user.idPaziente, user.id)
    ex = False
    try:
        user_from_db.getPazienteByID(manager.db, delete=True)
    except RowNotFoundException:
        assert False, "The user should be found in the DB before getting deleted"
    try:
        user.getPazienteByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The user should NOT be found in the DB"


def test_positive_auth():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                    "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user_from_db = Paziente(codiceFiscale="CF", password="password")
    try:
        user_from_db.authPaziente(manager.db)
    except RowNotFoundException:
        assert False, "The user should be found in the DB"
    assert user == user_from_db, "Should be the same user"
    try:
        user.getPazienteByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_wrong_password():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                    "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user_from_db = Paziente(codiceFiscale="CF", password="trying_a_password")
    ex = False
    try:
        user_from_db.authPaziente(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "Authentication should not pass"
    try:
        user.getPazienteByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_wrong_cf():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                    "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user_from_db = Paziente(codiceFiscale="asd", password="password")
    ex = False
    try:
        user_from_db.authPaziente(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "Authentication should not pass"
    try:
        user.getPazienteByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_insert_user_already_exist():
    user = Paziente(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                  "password", "CF", "tessera", "roma")
    user.addPaziente(manager.db)
    user2 = Paziente(0, 0, "carlo", "bianchi", datetime.date(1980, 4, 25), "roma", "carlo.b@lol.it", "123456789",
                    "password", "CF", "tessera", "roma")
    ex = False
    try:
        user2.addPaziente(manager.db)
    except AlreadyExistException:
        ex = True
    assert ex, "Paziente with that codiceFiscale and/or tesseraSanitaria should already be existing"
    try:
        user.getPazienteByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


tests = [test_insert_and_get, test_multiple_ins_and_get_and_compare, test_user_not_in_db, test_get_after_delete,
         test_positive_auth, test_wrong_password, test_wrong_cf, test_insert_user_already_exist]

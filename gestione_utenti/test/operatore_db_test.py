import sys
import datetime

sys.path.insert(0, "..")
from app_singleton import App

# in-memory database
manager = App(__name__, config={'db': "sqlite://", 'secret': '', 'session_validity_days': 1})

# need this import for db.create_all()
from utenteDAO import UtenteDAO
from operatoreDAO import OperatoreDAO
from operatore import Operatore
from appExceptions import RowNotFoundException, AlreadyExistException

manager.db.create_all()


def test_insert_and_get():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user_from_db = Operatore(user.idOperatore, user.id)
    try:
        user_from_db.getOperatoreByID(manager.db)
    except RowNotFoundException:
        assert False, "The user should be found in the DB"
    assert user == user_from_db, "Should be the same user"
    try:
        user.getOperatoreByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_multiple_ins_and_get_and_compare():
    mario = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                      "password", "asl0")
    mario.addOperatore(manager.db)
    claudia = Operatore(0, 0, "claudia", "verdi", datetime.date(1982, 5, 17), "roma", "cla.verdi@lol.it", "123456788",
                        "strong_password", "asl1")
    claudia.addOperatore(manager.db)
    mario_from_db = Operatore(mario.idOperatore, mario.id)
    mario_from_db.getOperatoreByID(manager.db)
    claudia_from_db = Operatore(claudia.idOperatore, claudia.id)
    claudia_from_db.getOperatoreByID(manager.db)
    assert not (mario_from_db == claudia_from_db), "They should be different users"
    try:
        mario.getOperatoreByID(manager.db, delete=True)
        claudia.getOperatoreByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_user_not_in_db():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user_from_db = Operatore(user.idOperatore + 1, user.id)
    ex = False
    try:
        user_from_db.getOperatoreByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The user should NOT be found in the DB"
    try:
        user.getOperatoreByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_get_after_delete():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user_from_db = Operatore(user.idOperatore, user.id)
    ex = False
    try:
        user_from_db.getOperatoreByID(manager.db, delete=True)
    except RowNotFoundException:
        assert False, "The user should be found in the DB before getting deleted"
    try:
        user.getOperatoreByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The user should NOT be found in the DB"


def test_positive_auth():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user_from_db = Operatore(idAslOperatore="asl0", password="password")
    try:
        user_from_db.authOperatore(manager.db)
    except RowNotFoundException:
        assert False, "The user should be found in the DB"
    assert user == user_from_db, "Should be the same user"
    try:
        user.getOperatoreByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_wrong_password():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user_from_db = Operatore(idAslOperatore="asl0", password="trying_a_password")
    ex = False
    try:
        user_from_db.authOperatore(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "Authentication should not pass"
    try:
        user.getOperatoreByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_wrong_id_asl():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user_from_db = Operatore(idAslOperatore="asl1", password="password")
    ex = False
    try:
        user_from_db.authOperatore(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "Authentication should not pass"
    try:
        user.getOperatoreByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_insert_user_already_exist():
    user = Operatore(0, 0, "mario", "rossi", datetime.date(1980, 4, 25), "roma", "mario.rossi@lol.it", "123456789",
                     "password", "asl0")
    user.addOperatore(manager.db)
    user2 = Operatore(0, 0, "carlo", "bianchi", datetime.date(1980, 4, 25), "roma", "carlo.b@lol.it", "123456789",
                    "password", "asl0")
    ex = False
    try:
        user2.addOperatore(manager.db)
    except AlreadyExistException:
        ex = True
    assert ex, "Operatore with that idAslOperatore should already be existing"
    try:
        user.getOperatoreByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


tests = [test_insert_and_get, test_multiple_ins_and_get_and_compare, test_user_not_in_db, test_get_after_delete,
         test_positive_auth, test_wrong_password, test_wrong_id_asl, test_insert_user_already_exist]

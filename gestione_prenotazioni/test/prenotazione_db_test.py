import sys
import datetime

sys.path.insert(0, "..")
from app_singleton import App

# in-memory database
manager = App(__name__, config={'db': "sqlite://", 'secret': '', 'session_validity_days': 1})

# need this import for db.create_all()
from prenotazioneDAO import PrenotazioneDAO
from prenotazione import Prenotazione
from appExceptions import RowNotFoundException, AlreadyExistException

manager.db.create_all()


def test_insert_and_get_by_id():
    prenotazione = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                                "mario.rossi@lol.it", "123456789")
    prenotazione.addPrenotazione(manager.db)
    p_from_db = Prenotazione(prenotazione.id)
    try:
        p_from_db.getPrenotazioneByID(manager.db)
    except RowNotFoundException:
        assert False, "The booking should be found in the DB"
    assert prenotazione == p_from_db, "Should be the same booking"
    try:
        prenotazione.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_insert_and_get_by_codiceFiscale():
    prenotazione = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                                "mario.rossi@lol.it", "123456789")
    prenotazione.addPrenotazione(manager.db)
    p_from_db = Prenotazione(codiceFiscale=prenotazione.codiceFiscale)
    try:
        p_from_db.getPrenotazioneByCodiceFiscale(manager.db)
    except RowNotFoundException:
        assert False, "The booking should be found in the DB"
    assert prenotazione == p_from_db, "Should be the same booking"
    try:
        prenotazione.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_multiple_ins_and_get_and_compare():
    p1 = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                      "mario.rossi@lol.it", "123456789")
    p1.addPrenotazione(manager.db)
    p2 = Prenotazione(0, 1, "roma", datetime.date(2022, 1, 1), "cf2", "tessera2", "roma", "claudia", "verdi",
                      "cla.verdi@lol.it", "123456788")
    p2.addPrenotazione(manager.db)
    p1_from_db = Prenotazione(p1.id)
    p1_from_db.getPrenotazioneByID(manager.db)
    p2_from_db = Prenotazione(p2.id)
    p2_from_db.getPrenotazioneByID(manager.db)
    assert not (p1_from_db == p2_from_db), "They should be different bookings"
    try:
        p1.getPrenotazioneByID(manager.db, delete=True)
        p2.getPrenotazioneByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_booking_not_in_db_by_id():
    prenotazione = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                                "mario.rossi@lol.it", "123456789")
    prenotazione.addPrenotazione(manager.db)
    p_from_db = Prenotazione(prenotazione.id + 1)
    ex = False
    try:
        p_from_db.getPrenotazioneByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The booking should NOT be found in the DB"
    try:
        prenotazione.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_booking_not_in_db_by_codiceFiscale():
    prenotazione = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                                "mario.rossi@lol.it", "123456789")
    prenotazione.addPrenotazione(manager.db)
    p_from_db = Prenotazione(codiceFiscale="salt" + prenotazione.codiceFiscale)
    ex = False
    try:
        p_from_db.getPrenotazioneByCodiceFiscale(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The booking should NOT be found in the DB"
    try:
        prenotazione.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def get_after_delete():
    prenotazione = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                                "mario.rossi@lol.it", "123456789")
    prenotazione.addPrenotazione(manager.db)
    p_from_db = Prenotazione(prenotazione.id)
    ex = False
    try:
        p_from_db.getPrenotazioneByID(manager.db, delete=True)
    except RowNotFoundException:
        assert False, "The booking should be found in DB before getting deleted"
    try:
        p_from_db.getPrenotazioneByID(manager.db)
    except RowNotFoundException:
        ex = True
    assert ex, "The booking should NOT be found in the DB"
    try:
        prenotazione.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_insert_booking_already_exist():
    p1 = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                      "mario.rossi@lol.it", "123456789")
    p1.addPrenotazione(manager.db)
    # testing with same codiceFiscale and tesseraSanitaria
    p2 = Prenotazione(0, 1, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "claudia", "verdi",
                      "cla.verdi@lol.it", "123456788")
    ex = False
    try:
        p2.addPrenotazione(manager.db)
    except AlreadyExistException:
        ex = True
    assert ex, "Prenotazione with that personal identifiers should already be existing"
    try:
        p1.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_no_future_bookings():
    listaPrenotazioni = Prenotazione.getAllPrenotazioniFuture(manager.db)
    assert len(listaPrenotazioni) == 0, "The list should be empty"


def test_get_sorted_future_bookings():
    p1 = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                      "mario.rossi@lol.it", "123456789")
    p1.addPrenotazione(manager.db)
    p2 = Prenotazione(0, 1, "roma", datetime.date(2022, 1, 2), "cf2", "tessera2", "roma", "claudia", "verdi",
                      "cla.verdi@lol.it", "123456788")
    p2.addPrenotazione(manager.db)
    p3 = Prenotazione(0, 2, "roma", datetime.date(1984, 1, 1), "cf3", "tessera3", "roma", "carlo", "bianchi",
                      "c.bianchi@lol.it", "123456787")
    p3.addPrenotazione(manager.db)
    listaPrenotazioni = Prenotazione.getAllPrenotazioniFuture(manager.db)
    assert len(listaPrenotazioni) > 0, "The list must not be empty"
    assert p1 in listaPrenotazioni, "Future bookings should be in the queried list"
    assert p2 in listaPrenotazioni, "Future bookings should be in the queried list"
    assert p3 not in listaPrenotazioni, "Past bookings should NOT be in the queried list"
    assert listaPrenotazioni[0].dataVaccino < listaPrenotazioni[1].dataVaccino, \
        "The list should be sorted in ascending order by dataVaccino"
    try:
        p1.getPrenotazioneByID(manager.db, delete=True)
        p2.getPrenotazioneByID(manager.db, delete=True)
        p3.getPrenotazioneByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


def test_create_and_get_scheduled_booking():
    prenotazione = Prenotazione(0, 0, "roma", datetime.date(1900, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                                "mario.rossi@lol.it", "123456789")
    prenotazione.creaNuovaPrenotazione(manager.db)
    p_from_db = Prenotazione(prenotazione.id)
    try:
        p_from_db.getPrenotazioneByID(manager.db)
    except RowNotFoundException:
        assert False, "The booking should be found in the DB"
    assert prenotazione == p_from_db, "Should be the same booking"
    assert prenotazione.dataVaccino > datetime.date.today(), "The scheduling should be in the future"
    try:
        prenotazione.getPrenotazioneByID(manager.db, delete=True)  # cleanup
    except RowNotFoundException:
        pass


def test_create_and_get_scheduled_booking_with_time_slot_overflow():
    maxBookingsPerDay = 2
    p1 = Prenotazione(0, 0, "roma", datetime.date(2022, 1, 1), "cf", "tessera", "roma", "mario", "rossi",
                      "mario.rossi@lol.it", "123456789")
    p1.creaNuovaPrenotazione(manager.db, maxBookingsPerDay=maxBookingsPerDay)
    p2 = Prenotazione(0, 1, "roma", datetime.date(2022, 1, 2), "cf2", "tessera2", "roma", "claudia", "verdi",
                      "cla.verdi@lol.it", "123456788")
    p2.creaNuovaPrenotazione(manager.db, maxBookingsPerDay=maxBookingsPerDay)
    p3 = Prenotazione(0, 2, "roma", datetime.date(1984, 1, 1), "cf3", "tessera3", "roma", "carlo", "bianchi",
                      "c.bianchi@lol.it", "123456787")
    p3.creaNuovaPrenotazione(manager.db, maxBookingsPerDay=maxBookingsPerDay)
    assert p1.dataVaccino == p2.dataVaccino, "The scheduling should occupy all available time slots"
    assert p3.dataVaccino == p1.dataVaccino + datetime.timedelta(days=1),\
        "The scheduling should handle time slot overflow in a predictable way"
    try:
        p1.getPrenotazioneByID(manager.db, delete=True)
        p2.getPrenotazioneByID(manager.db, delete=True)
        p3.getPrenotazioneByID(manager.db, delete=True)
    except RowNotFoundException:
        pass


tests = [test_insert_and_get_by_id, test_insert_and_get_by_codiceFiscale, test_multiple_ins_and_get_and_compare,
         test_booking_not_in_db_by_id, test_booking_not_in_db_by_codiceFiscale, get_after_delete,
         test_insert_booking_already_exist, test_no_future_bookings, test_get_sorted_future_bookings,
         test_create_and_get_scheduled_booking, test_create_and_get_scheduled_booking_with_time_slot_overflow]


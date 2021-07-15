from app_singleton import App

manager = App(__name__, "./volume/config.json")

import projectUtils
# need this import to create the table
from prenotazioneDAO import PrenotazioneDAO

app = manager.app

db_path = manager.config['db']
if not projectUtils.check_db(db_path):
    manager.db.create_all()

from prenotazione import Prenotazione
from flask import session
from mock_gestione_turni import verificaFinestraTemporale
import datetime
from appExceptions import AlreadyExistException, RowNotFoundException


def logged_in(user):
    if user['is_operatore']:
        return projectUtils.info_msg("You are logged with idAslOperatore {}".format(user['idAslOperatore']))
    else:
        return projectUtils.info_msg("You are logged with codiceFiscale {}".format(user['codiceFiscale']))


@app.errorhandler(Exception)
def unexpectedExceptionHandler(error):
    return projectUtils.exceptionHandler("Unexpected exception", error)


@app.errorhandler(404)
def NotFoundHandler(error):
    return projectUtils.exceptionHandler("404 Not Found", error)


@app.errorhandler(500)
def ServerErrorHandler(error):
    return projectUtils.exceptionHandler("500 Internal Server Error", error)


@app.route('/', methods=['GET'])
@app.route('/api/bookings', methods=['GET'], strict_slashes=False)
def index():
    if 'user' not in session:
        return projectUtils.info_msg("Service is up")
    else:
        user = projectUtils.data_from_cookie(session['user'])
        return logged_in(user)


@app.route('/api/bookings/newBooking', methods=['POST'], strict_slashes=False)
def booking():
    if 'user' not in session:
        return projectUtils.error_msg("You must login to make a Prenotazione")
    user = projectUtils.data_from_cookie(session['user'])
    try:
        if user['is_operatore']:
            return projectUtils.error_msg("You can't make a Prenotazione as an Operatore; please login using your "
                                          "Paziente account")
    except KeyError:
        projectUtils.log(logType='Security', message="cookie was tampered")
        return projectUtils.error_msg("Some required values missing")
    try:
        dataNascita = [int(i) for i in user['dataNascita'].split('-')]
        user['dataNascita'] = datetime.date(*dataNascita)
    except:
        projectUtils.log(logType='Security', message="cookie was tampered")
        return projectUtils.error_msg("Bad 'dataNascita' field")
    etaPaziente = datetime.date.today().year - user['dataNascita'].year
    checkWindow, startWindow = verificaFinestraTemporale(etaPaziente)
    if not checkWindow:
        return projectUtils.error_msg("Sorry, it's too early for you to make a Prenotazione. Come back later "
                                      "starting from: {}".format(str(startWindow)))
    deltaDays = manager.config['deltaDays']
    maxBookingsPerDay = manager.config['maxBookingsPerDay']
    try:
        prenotazione = Prenotazione(_id=0, idPaziente=user['idPaziente'], codiceFiscale=user['codiceFiscale'],
                                    tesseraSanitaria=user['tesseraSanitaria'], luogoResidenza=user['luogoResidenza'],
                                    nome=user['nome'], cognome=user['cognome'], email=user['email'],
                                    telefono=user['telefono'])
        prenotazione.creaNuovaPrenotazione(manager.db, deltaDays=deltaDays, maxBookingsPerDay=maxBookingsPerDay)
        success_msg = projectUtils.success_msg("Prenotazione added", prenotazione.__dict__)
        return success_msg
    except AlreadyExistException:
        return projectUtils.error_msg("Tried to add a 'prenotazione' for a 'paziente' who already added one.")
    except KeyError:
        projectUtils.log(logType='Security', message="cookie was tampered")
        return projectUtils.error_msg("Some required values missing")


@app.route('/api/bookings/view', methods=['GET'], strict_slashes=False)
def view():
    if 'user' not in session:
        return projectUtils.error_msg("You must login to access this API")
    user = projectUtils.data_from_cookie(session['user'])
    try:
        if user['is_operatore']:
            listaPrenotazioni = Prenotazione.getAllPrenotazioniFuture(manager.db)
            listaPrenotazioni = [p.__dict__ for p in listaPrenotazioni]
            success_msg = projectUtils.success_msg("Here is the list of future bookings, sorted by dataVaccino "
                                                   "in ascending order", listaPrenotazioni)
            return success_msg
        else:
            prenotazione = Prenotazione(codiceFiscale=user['codiceFiscale'])
            prenotazione.getPrenotazioneByCodiceFiscale(manager.db)
            success_msg = projectUtils.success_msg("Prenotazione found", prenotazione.__dict__)
            return success_msg
    except KeyError:
        projectUtils.log(logType='Security', message="cookie was tampered")
        return projectUtils.error_msg("Some required values missing")
    except RowNotFoundException:
        return projectUtils.info_msg("You haven't made a Prenotazione yet")


if __name__ == '__main__':
    app.run(debug=manager.config['debug'], host="0.0.0.0", port=manager.config['port'])

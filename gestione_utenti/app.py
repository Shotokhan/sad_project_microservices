from app_singleton import App

manager = App(__name__, "./volume/config.json")

import projectUtils
# need these imports to create tables
from utenteDAO import UtenteDAO
from pazienteDAO import PazienteDAO
from operatoreDAO import OperatoreDAO

db_path = manager.config['db']
if not projectUtils.check_db(db_path):
    manager.db.create_all()

from paziente import Paziente
from operatore import Operatore
from stubs_sistemi_esterni import verifyPaziente, verifyLuogo
import datetime
from flask import request, session
from appExceptions import AlreadyExistException, RowNotFoundException

app = manager.app


def already_logged_in(user):
    if user['is_operatore']:
        return projectUtils.info_msg("You are already logged with idAslOperatore {}".format(user['idAslOperatore']))
    else:
        return projectUtils.info_msg("You are already logged with codiceFiscale {}".format(user['codiceFiscale']))


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
@app.route('/api/users', methods=['GET'], strict_slashes=False)
def index():
    if 'user' not in session:
        return projectUtils.info_msg("Service is up")
    else:
        user = projectUtils.data_from_cookie(session['user'])
        return already_logged_in(user)


@app.route('/api/users/register', methods=['POST'], strict_slashes=False)
def register():
    # only a Paziente can register using the API, Operatore is added occasionally by an admin
    """
    Input is like:
     data =
     {'nome': 'a', 'cognome': 'b', 'dataNascita': '2020-1-1', 'luogoNascita': 'n', 'email': 'c', 'telefono': 'd',
     'password': 'pass', 'codiceFiscale': 'cf', 'tesseraSanitaria': 'ts', 'luogoResidenza': 'n'}
    Test from python shell:
     url = "http://{}:{}/api/users/register".format(ip, port)

     r = requests.post(url, json=data)
    """
    if 'user' in session:
        user = projectUtils.data_from_cookie(session['user'])
        return already_logged_in(user)
    params = request.get_json()
    try:
        try:
            dataNascita = [int(i) for i in params['dataNascita'].split('-')]
            params['dataNascita'] = datetime.date(*dataNascita)
        except:
            return projectUtils.error_msg("Bad 'dataNascita' field")
        user = Paziente(0, 0, params['nome'], params['cognome'], params['dataNascita'], params['luogoNascita'],
                        params['email'], params['telefono'], params['password'], params['codiceFiscale'],
                        params['tesseraSanitaria'], params['luogoResidenza'])
        verificaAnagrafica = verifyPaziente(user)
        verificaLuogo = verifyLuogo(user.luogoNascita) and verifyLuogo(user.luogoResidenza)
        if not (verificaAnagrafica and verificaLuogo):
            return projectUtils.error_msg("Problems with some input data; anagrafica: {}, "
                                          "luogo nascita/residenza: {}".format(verificaAnagrafica, verificaLuogo))
        user.addPaziente(manager.db)
        success_msg = projectUtils.success_msg("Success: account created", user.__dict__)
        session.permanent = True
        session['user'] = projectUtils.cookie_data(user.__dict__, is_operatore=False)
        return success_msg
    except AlreadyExistException:
        return projectUtils.error_msg("Paziente with that codiceFiscale and/or tesseraSanitaria already exists")
    except KeyError:
        return projectUtils.error_msg("Some required values missing")


@app.route('/api/users/login', methods=['POST'], strict_slashes=False)
def login():
    """
    Input is like:
     data = {'codiceFiscale': 'cf', 'password': 'pass', 'is_operatore': False}
    OR
     data = {'idAslOperatore': 'asl0', 'password': 'pass', 'is_operatore': True}
    Test from python shell:
     base_url = "http://{}:{}".format(ip, port)

     s = requests.Session()

     r1 = s.post(base_url + "/api/users/login", json=data)

     r2 = s.get(base_url + "/")
    """
    if 'user' in session:
        user = projectUtils.data_from_cookie(session['user'])
        return already_logged_in(user)
    params = request.get_json()
    try:
        if params['is_operatore']:
            user = Operatore(idAslOperatore=params['idAslOperatore'], password=params['password'])
            user.authOperatore(manager.db)
        else:
            user = Paziente(codiceFiscale=params['codiceFiscale'], password=params['password'])
            user.authPaziente(manager.db)
        success_msg = projectUtils.success_msg("Login successful", user.__dict__)
        session.permanent = True
        session['user'] = projectUtils.cookie_data(user.__dict__, is_operatore=params['is_operatore'])
        return success_msg
    except RowNotFoundException:
        return projectUtils.error_msg("Login failed")
    except KeyError:
        return projectUtils.error_msg("Some required values missing")


@app.route('/api/users/logout', methods=['GET'], strict_slashes=False)
def logout():
    if 'user' in session:
        _keys = [key for key in session.keys()]
        [session.pop(key) for key in _keys]
        return projectUtils.info_msg("Logged out")
    else:
        return projectUtils.error_msg("You are not logged in")


if __name__ == '__main__':
    app.run(debug=manager.config['debug'], host="0.0.0.0", port=manager.config['port'])

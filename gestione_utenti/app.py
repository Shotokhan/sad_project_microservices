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
from flask import request
from appExceptions import AlreadyExistException

app = manager.app


@app.route('/', methods=['GET'])
def index():
    return "Service is up"


@app.route('/api/register', methods=['POST'])
def register():
    # only a Paziente can register using the API, Operatore is added occasionally by an admin
    """
    Input is like:
     data =
     {'nome': 'a', 'cognome': 'b', 'dataNascita': '2020-1-1', 'luogoNascita': 'n', 'email': 'c', 'telefono': 'd',
     'password': 'pass', 'codiceFiscale': 'cf', 'tesseraSanitaria': 'ts', 'luogoResidenza': 'n'}
    Test from python shell:
     url = "http://{}:{}/api/register".format(ip, port)

     r = requests.post(url, json=data)
    """
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
        # TODO: set cookie (a function for it)
        return success_msg
    except AlreadyExistException:
        return projectUtils.error_msg("Paziente with that codiceFiscale and/or tesseraSanitaria already exists")
    except KeyError:
        return projectUtils.error_msg("Some required values missing")

# TODO: login


if __name__ == '__main__':
    app.run(debug=manager.config['debug'], host="0.0.0.0", port=manager.config['port'])

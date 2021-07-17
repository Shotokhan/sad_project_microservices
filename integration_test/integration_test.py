import requests
import json
import uuid
import hashlib
import datetime

config = {}
with open('./config.json', 'r') as f:
    config = json.load(f)
assert len(config) > 0, "Configuration file cannot be empty"

url = "http://{}:{}".format(config['ip'], config['port'])
gatewayStatus = url + "/api/gateway/status"
usersAPI = url + "/api/users"
bookingsAPI = url + "/api/bookings"
register = usersAPI + "/register"
login = usersAPI + "/login"
logout = usersAPI + "/logout"
newBooking = bookingsAPI + "/newBooking"
view = bookingsAPI + "/view"

_timeout = 2
apiStatusCodes = {'info': 200, 'success': 201, 'error': 400}
statusCodeErrorMsg = "Status code should be {}"


# I won't catch exceptions, they give me enough info

def str_to_datetime(dataNascita):
    dataNascita = [int(i) for i in dataNascita.split('-')]
    return datetime.date(*dataNascita)


def hash_pw(password):
    h = hashlib.sha256()
    h.update(password.encode())
    return h.hexdigest()


def util_random_uuid():
    return str(uuid.uuid4())


def test_gateway_up():
    r = requests.get(gatewayStatus, timeout=_timeout)
    j = json.loads(r.text)
    assert j['info'] == 'Service is up', "The gateway should be up"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])


def test_users_api_up():
    r = requests.get(usersAPI, timeout=_timeout, allow_redirects=True)
    j = json.loads(r.text)
    assert j['info'] == 'Service is up', "'gestione_utenti' should be up"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])


def test_bookings_api_up():
    r = requests.get(bookingsAPI, timeout=_timeout, allow_redirects=True)
    j = json.loads(r.text)
    assert j['info'] == 'Service is up', "'gestione_prenotazioni' should be up"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])


def test_registration_successful_paziente():
    codiceFiscale = util_random_uuid()
    data = {'nome': 'a', 'cognome': 'b', 'dataNascita': '1900-1-1', 'luogoNascita': 'n', 'email': 'c',
            'telefono': 'd', 'password': 'pass', 'codiceFiscale': codiceFiscale,
            'tesseraSanitaria': util_random_uuid(), 'luogoResidenza': 'n'}
    s = requests.Session()
    r = s.post(register, json=data)
    j = json.loads(r.text)
    assert 'success' in j, "Registration should be successful"
    assert r.status_code == apiStatusCodes['success'], statusCodeErrorMsg.format(apiStatusCodes['success'])
    received = j['data']
    data['password'] = hash_pw(data['password'])
    data['dataNascita'] = str_to_datetime(data['dataNascita'])
    received['dataNascita'] = str_to_datetime(received['dataNascita'])
    for _key in data.keys():
        assert data[_key] == received[_key], "Input {} should be equal to the received one".format(_key)
    assert len(s.cookies) == 1, "A cookie should have been set"
    return s, data


def test_registration_failed_missing_field():
    codiceFiscale = util_random_uuid()
    data = {'nome': 'a', 'cognome': 'b', 'dataNascita': '2020-1-1', 'luogoNascita': 'n', 'email': 'c',
            'telefono': 'd', 'password': 'pass', 'codiceFiscale': codiceFiscale,
            'tesseraSanitaria': util_random_uuid()}
    s = requests.Session()
    r = s.post(register, json=data)
    j = json.loads(r.text)
    assert 'error' in j, "Registration should not be allowed if some required field is missing"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_registration_failed_bad_birth_date():
    codiceFiscale = util_random_uuid()
    data = {'nome': 'a', 'cognome': 'b', 'dataNascita': '2020-2020-1', 'luogoNascita': 'n', 'email': 'c',
            'telefono': 'd', 'password': 'pass', 'codiceFiscale': codiceFiscale,
            'tesseraSanitaria': util_random_uuid(), 'luogoResidenza': 'n'}
    s = requests.Session()
    r = s.post(register, json=data)
    j = json.loads(r.text)
    assert 'error' in j, "Registration should not be allowed if birth date is not a valid YYYY-MM-DD date"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_registration_failed_already_existing_paziente():
    s1, data_1 = test_registration_successful_paziente()
    data_2 = data_1.copy()
    # same codiceFiscale
    data_2['password'], data_2['tesseraSanitaria'] = 'pass', util_random_uuid()
    data_2['dataNascita'] = str(data_2['dataNascita'])
    s2 = requests.Session()
    r = s2.post(register, json=data_2)
    j = json.loads(r.text)
    assert 'error' in j, "Registration should not be allowed if there is an existing Paziente with the" \
                         " same unique data"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_login_successful_with_session_paziente():
    s, data = test_registration_successful_paziente()
    r = s.post(login)
    j = json.loads(r.text)
    assert 'info' in j, "Response message should be an info message to say that you're already logged in"
    assert 'codiceFiscale' in j['info'], "The user should be logged in as a Paziente"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])


def test_login_successful_without_session_paziente():
    s, data = test_registration_successful_paziente()
    loginData = {"codiceFiscale": data['codiceFiscale'], "password": "pass", "is_operatore": False}
    r = requests.post(login, json=loginData)
    j = json.loads(r.text)
    assert 'success' in j, "Login should be successful"
    assert r.status_code == apiStatusCodes['success'], statusCodeErrorMsg.format(apiStatusCodes['success'])
    received = j['data']
    received['dataNascita'] = str_to_datetime(received['dataNascita'])
    for _key in data.keys():
        assert data[_key] == received[_key], "Registration {} should be equal to the received one" \
                                             " after login".format(_key)
    assert len(r.cookies) == 1, "A cookie should have been set"


def test_login_failed_wrong_password_paziente():
    s, data = test_registration_successful_paziente()
    loginData = {"codiceFiscale": data['codiceFiscale'], "password": "WRONG", "is_operatore": False}
    r = requests.post(login, json=loginData)
    j = json.loads(r.text)
    assert 'error' in j, "Login should fail if password is wrong"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_login_failed_wrong_codiceFiscale_paziente():
    s, data = test_registration_successful_paziente()
    loginData = {"codiceFiscale": util_random_uuid(), "password": "pass", "is_operatore": False}
    r = requests.post(login, json=loginData)
    j = json.loads(r.text)
    assert 'error' in j, "Login should fail if codiceFiscale is wrong (i.e. not existing user)"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_login_failed_missing_required_field_paziente():
    s, data = test_registration_successful_paziente()
    loginData = {"codiceFiscale": data['codiceFiscale'], "password": "pass"}
    r = requests.post(login, json=loginData)
    j = json.loads(r.text)
    assert 'error' in j, "Login should fail if some required field is missing"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_login_successful_without_session_operatore():
    loginData = {"idAslOperatore": "asl0", "password": "pass", "is_operatore": True}
    s = requests.Session()
    r = s.post(login, json=loginData)
    j = json.loads(r.text)
    assert 'success' in j, \
        "Check if an Operatore with idAslOperatore {} and password {} exists on the database," \
        " if not then create it manually and then execute the test again. If the error" \
        " persists, then the test is failed".format(loginData['idAslOperatore'], loginData['password'])
    assert r.status_code == apiStatusCodes['success'], statusCodeErrorMsg.format(apiStatusCodes['success'])
    received = j['data']
    assert received['idAslOperatore'] == loginData['idAslOperatore'], \
        "You should have been logged in as {}".format(loginData['idAslOperatore'])
    assert len(s.cookies) == 1, "A cookie should have been set"
    return s, received


def test_login_successful_with_session_operatore():
    s, data = test_login_successful_without_session_operatore()
    r = s.post(login)
    j = json.loads(r.text)
    assert 'info' in j, "Response message should be an info message to say that you're already logged in"
    assert 'idAslOperatore' in j['info'], "The user should be logged in as an Operatore"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])


def test_logout_ok_paziente():
    s, data = test_registration_successful_paziente()
    r = s.get(logout)
    j = json.loads(r.text)
    assert 'info' in j, "Response message should be an info message to say that you were logged out"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])
    assert len(r.cookies) == 0 and len(s.cookies) == 0, "Cookie should have been removed from session"


def test_logout_error():
    r = requests.get(logout)
    j = json.loads(r.text)
    assert 'error' in j, "Response message should be an error message because you tried to logout without a" \
                         " session cookie"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])
    assert len(r.cookies) == 0, "A logout endpoint shouldn't set a cookie"


def test_logout_ok_operatore():
    s, data = test_login_successful_without_session_operatore()
    r = s.get(logout)
    j = json.loads(r.text)
    assert 'info' in j, "Response message should be an info message to say that you were logged out"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])
    assert len(r.cookies) == 0 and len(s.cookies) == 0, "Cookie should have been removed from session"


def test_view_booking_not_logged():
    r = requests.get(view)
    j = json.loads(r.text)
    assert 'error' in j, "Each user has to log-in before viewing bookings"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_view_booking_not_made_yet():
    s, data = test_registration_successful_paziente()
    r = s.get(view)
    j = json.loads(r.text)
    assert 'info' in j, "Response message should be an info message to say that you haven't made a Prenotazione yet"
    assert r.status_code == apiStatusCodes['info'], statusCodeErrorMsg.format(apiStatusCodes['info'])


def test_new_booking_successful():
    s, data = test_registration_successful_paziente()
    r = s.post(newBooking)
    j = json.loads(r.text)
    assert 'success' in j, "Prenotazione should have been allowed; if not, check input dataNascita field: " \
                           "{}".format(str(data['dataNascita']))
    assert r.status_code == apiStatusCodes['success'], statusCodeErrorMsg.format(apiStatusCodes['success'])
    received = j['data']
    commonKeys = set(data.keys()).intersection(set(received.keys()))
    for _key in commonKeys:
        assert data[_key] == received[_key], "Common fields between Paziente and Prenotazione should be coherent"
    dataVaccino = str_to_datetime(received['dataVaccino'])
    assert dataVaccino > datetime.date.today(), "Prenotazione should be scheduled in the future"
    return s, received


def test_booking_already_made():
    s, data = test_new_booking_successful()
    r = s.post(newBooking)
    j = json.loads(r.text)
    assert 'error' in j, "Prenotazione should not be allowed for an user who already added one"
    assert r.status_code == apiStatusCodes['error'], statusCodeErrorMsg.format(apiStatusCodes['error'])


def test_view_booking_paziente():
    s, data = test_new_booking_successful()
    r = s.get(view)
    j = json.loads(r.text)
    assert 'success' in j, "There should be an existing Prenotazione for that Paziente"
    assert r.status_code == apiStatusCodes['success'], statusCodeErrorMsg.format(apiStatusCodes['success'])
    received = j['data']
    data['dataVaccino'] = str_to_datetime(data['dataVaccino'])
    received['dataVaccino'] = str_to_datetime(received['dataVaccino'])
    for _key in data.keys():
        assert data[_key] == received[_key], "Prenotazione viewed should be equal to the one created"


def test_view_bookings_operatore():
    s, data = test_login_successful_without_session_operatore()
    _, p1 = test_new_booking_successful()
    _, p2 = test_new_booking_successful()
    r = s.get(view)
    j = json.loads(r.text)
    assert 'success' in j, "A logged Operatore should be able to access the /bookings/view API"
    assert r.status_code == apiStatusCodes['success'], statusCodeErrorMsg.format(apiStatusCodes['success'])
    received = j['data']
    assert isinstance(received, list), "Returned data should be a list of Prenotazione dictionaries"
    assert len(received) >= 2, "There should be at least 2 Prenotazione on the DB"
    p1_ok, p2_ok = False, False
    for p in received:
        if p['codiceFiscale'] == p1['codiceFiscale']:
            p1_ok = True
        elif p['codiceFiscale'] == p2['codiceFiscale']:
            p2_ok = True
    assert p1_ok and p2_ok, "The Operatore should be able to view the just added Prenotazione objects"


tests = [test_gateway_up, test_users_api_up, test_bookings_api_up, test_registration_successful_paziente,
         test_registration_failed_missing_field, test_registration_failed_bad_birth_date,
         test_registration_failed_already_existing_paziente, test_login_successful_with_session_paziente,
         test_login_successful_without_session_paziente, test_login_failed_wrong_password_paziente,
         test_login_failed_wrong_codiceFiscale_paziente, test_login_failed_missing_required_field_paziente,
         test_login_successful_without_session_operatore, test_login_successful_with_session_operatore,
         test_logout_ok_paziente, test_logout_error, test_logout_ok_operatore, test_view_booking_not_logged,
         test_view_booking_not_made_yet, test_new_booking_successful, test_booking_already_made,
         test_view_booking_paziente, test_view_bookings_operatore]

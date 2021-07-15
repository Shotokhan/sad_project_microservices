import requests
import json

config = {}
with open('./config.json', 'r') as f:
    config = json.load(f)
assert len(config) > 0, "Configuration file cannot be empty"

url = "http://{}:{}".format(config['ip'], config['port'])
usersAPI = url + "/api/users/"
bookingsAPI = url + "/api/bookings/"
register = usersAPI + "/register"
login = usersAPI + "/login"
logout = usersAPI + "/logout"
newBooking = bookingsAPI + "/newBooking"
view = bookingsAPI + "/view"

_timeout = 2

# I won't catch exceptions, they give me enough info


def test_gateway_up():
    r = requests.get(url, timeout=_timeout)
    j = json.loads(r.text)
    assert j['info'] == 'Service is up', "The gateway should be up"


def test_users_api_up():
    r = requests.get(usersAPI, timeout=_timeout, allow_redirects=True)
    j = json.loads(r.text)
    assert j['info'] == 'Service is up', "'gestione_utenti' should be up"


def test_bookings_api_up():
    r = requests.get(bookingsAPI, timeout=_timeout, allow_redirects=True)
    j = json.loads(r.text)
    assert j['info'] == 'Service is up', "'gestione_prenotazioni' should be up"


tests = [test_gateway_up, test_users_api_up, test_bookings_api_up]

import sys
sys.path.insert(0, "..")
from app_singleton import App
import requests_mock
import projectUtils


manager = App(__name__, config={
    "port": 5000,
    "debug": True,
    "gestione_utenti_url": "http://172.22.0.2:5000",
    "gestione_prenotazioni_url": "http://172.23.0.2:5000",
    "requests_timeout": 2
})
# need this *-import to init routes
from app import *
manager.app.config['TESTING'] = True

apiUsers = manager.gestioneUtentiURL + '/api/users/'
apiBookings = manager.gestionePrenotazioniURL + '/api/bookings/'
register = apiUsers + '/register'
login = apiUsers + '/login'
logout = apiUsers + '/logout'
newBooking = apiBookings + '/newBooking'
view = apiBookings + '/view'


def test_users_service_up():
    # doesn't work for some reason
    with requests_mock.Mocker() as mock:
        mock.get(apiUsers, text=projectUtils.info_msg("Service is up"))
        with manager.app.test_client() as client:
            res = client.get('/api/users/')
            data = res.get_json()
            assert data['info'] == "Service is up"


tests = []

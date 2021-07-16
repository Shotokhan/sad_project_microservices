from app_singleton import App
import requests
import projectUtils
from flask import Response, request, render_template, send_from_directory, redirect
import os


manager = App(__name__, "./volume/config.json")

app = manager.app
_timeout = manager.config['requests_timeout']


@app.errorhandler(Exception)
def unexpectedExceptionHandler(error):
    return projectUtils.exceptionHandler("Unexpected exception", error)


@app.errorhandler(404)
def NotFoundHandler(error):
    return projectUtils.exceptionHandler("404 Not Found", error)


@app.errorhandler(500)
def ServerErrorHandler(error):
    return projectUtils.exceptionHandler("500 Internal Server Error", error)


def gateway(url, path, incomingRequest):
    headers = dict(incomingRequest.headers)
    cookies = dict(incomingRequest.cookies)
    try:
        if incomingRequest.method == 'GET':
            r = requests.get(url + path, headers=headers, cookies=cookies, timeout=_timeout)
        elif incomingRequest.method == 'POST':
            data = incomingRequest.get_json(silent=True)
            if data is None:
                r = requests.post(url + path, headers=headers, cookies=cookies, timeout=_timeout)
            else:
                r = requests.post(url + path, json=data, headers=headers, cookies=cookies, timeout=_timeout)
        else:
            return projectUtils.info_msg("Supported methods: GET, POST")
        r_headers = [(name, value) for (name, value) in r.raw.headers.items()]
        res = Response(r.text, r.status_code, r_headers)
        return res, r
    except requests.exceptions.RequestException as e:
        return projectUtils.exceptionHandler("Exception while making a request to a microservice", e)


def pageForUser(urlForPaziente, urlForOperatore, urlForNotAuth):
    _, r = gateway(manager.gestioneUtentiURL, '/api/users', request)
    user = r.json()
    if 'info' in user:
        if 'codiceFiscale' in user['info']:
            return render_template(urlForPaziente)
        elif 'idAslOperatore' in user['info']:
            return render_template(urlForOperatore)
        else:
            return render_template(urlForNotAuth)
    else:
        return redirect('/errorPage', 302)


@app.route('/', methods=['GET'])
def index():
    return pageForUser('home.html', 'visualizza_prenotati.html', 'login.html')


@app.route('/api/gateway/status', methods=['GET'], strict_slashes=False)
def status():
    return projectUtils.info_msg("Service is up")


@app.route('/api/users', strict_slashes=False)
@app.route('/api/users/<path:path>', methods=['GET', 'POST'], strict_slashes=False)
def usersAPI(path=""):
    path = "/api/users/" + path
    url = manager.gestioneUtentiURL
    res, _ = gateway(url, path, request)
    return res


@app.route('/api/bookings', strict_slashes=False)
@app.route('/api/bookings/<path:path>', methods=['GET', 'POST'], strict_slashes=False)
def bookingsAPI(path=""):
    path = "/api/bookings/" + path
    url = manager.gestionePrenotazioniURL
    res, _ = gateway(url, path, request)
    return res


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'), 'favicon.png', mimetype='image/png')


@app.route('/errorPage', methods=['GET'])
def errorPage():
    if request.args is None:
        return render_template('error.html', error_msg="Unknown error")
    else:
        error_msg = request.args.get('error_msg')
        if error_msg is None:
            return render_template('error.html', error_msg="Unknown error")
        else:
            return render_template('error.html', error_msg=error_msg)


@app.route('/effettuaPrenotazione', methods=['GET'])
def newBooking():
    return pageForUser('effettua_prenotazione.html', 'visualizza_prenotati.html', 'login.html')


@app.route('/visualizzaPrenotazione', methods=['GET'])
def viewBooking():
    return pageForUser('visualizza_prenotazione.html', 'visualizza_prenotati.html', 'login.html')


@app.route('/registrazione', methods=['GET'])
def signUp():
    return pageForUser('home.html', 'visualizza_prenotati.html', 'registrazione.html')


if __name__ == '__main__':
    app.run(debug=manager.config['debug'], host="0.0.0.0", port=manager.config['port'])

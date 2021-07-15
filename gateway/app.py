from app_singleton import App
import requests
import projectUtils
from flask import Response, request

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
        return res
    except requests.exceptions.RequestException as e:
        return projectUtils.exceptionHandler("Exception while making a request to a microservice", e)


@app.route('/', methods=['GET'])
def index():
    return projectUtils.info_msg("Service is up")


@app.route('/api/users', strict_slashes=False)
@app.route('/api/users/<path:path>', methods=['GET', 'POST'], strict_slashes=False)
def usersAPI(path=""):
    path = "/api/users/" + path
    url = manager.gestioneUtentiURL
    return gateway(url, path, request)


@app.route('/api/bookings', strict_slashes=False)
@app.route('/api/bookings/<path:path>', methods=['GET', 'POST'], strict_slashes=False)
def bookingsAPI(path=""):
    path = "/api/bookings/" + path
    url = manager.gestionePrenotazioniURL
    return gateway(url, path, request)


if __name__ == '__main__':
    app.run(debug=manager.config['debug'], host="0.0.0.0", port=manager.config['port'])

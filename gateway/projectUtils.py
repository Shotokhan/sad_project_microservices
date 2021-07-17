import json
import flask


def log(logType, message):
    print("{} log: {}".format(logType, message))


def json_response(_json, status_code=200):
    return flask.Response(_json, mimetype='application/json', status=status_code)


def error_msg(message):
    d = {"error": message}
    return json_response(json.dumps(d, default=str), status_code=400)


def success_msg(message, data):
    # data is not "date"
    d = {"success": message, "data": data}
    return json_response(json.dumps(d, default=str), status_code=201)


def info_msg(message):
    d = {"info": message}
    return json_response(json.dumps(d, default=str))


def exceptionHandler(message, errorObj):
    log("Exception", str(errorObj))
    return error_msg(message)

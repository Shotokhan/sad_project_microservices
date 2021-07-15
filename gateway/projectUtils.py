import json
import flask


def log(logType, message):
    print("{} log: {}".format(logType, message))


def json_response(_json):
    return flask.Response(_json, mimetype='application/json')


def error_msg(message):
    d = {"error": message}
    return json_response(json.dumps(d, default=str))


def success_msg(message, data):
    # data is not "date"
    d = {"success": message, "data": data}
    return json_response(json.dumps(d, default=str))


def info_msg(message):
    d = {"info": message}
    return json_response(json.dumps(d, default=str))


def exceptionHandler(message, errorObj):
    log("Exception", str(errorObj))
    return error_msg(message)

import os
import json
import flask


def check_db(db_path):
    # assuming serverless db
    db_path = db_path.split('/')[::-1]
    ind = db_path.index('')
    db_path = db_path[:ind][::-1]
    db_name = db_path[-1]
    db_path = "/" + "/".join(db_path[:-1])
    if db_name in os.listdir(db_path):
        return True
    else:
        return False


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


def data_from_cookie(data_str):
    unserialized = json.loads(data_str)
    return unserialized


def exceptionHandler(message, errorObj):
    log("Exception", str(errorObj))
    return error_msg(message)

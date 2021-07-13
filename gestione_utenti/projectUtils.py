import os
import hashlib
import json


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


def hash_pw(password):
    h = hashlib.sha256()
    h.update(password.encode())
    return h.hexdigest()


def check_pw_hash(password, stored_hash):
    # this function was only used for tests
    return hash_pw(password) == stored_hash


def error_msg(message):
    d = {"error": message}
    return json.dumps(d)


def success_msg(message, data):
    # data is not "date"
    d = {"success": message, "data": data}
    return json.dumps(d, default=str)

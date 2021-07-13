import sys
sys.path.insert(0, "..")
from projectUtils import hash_pw, check_pw_hash


def test_1():
    pw = "password"
    h = hash_pw(pw)
    check = check_pw_hash(pw, h)
    assert check, "Password should be right"


def test_2():
    pw = "password"
    h = hash_pw(pw)
    wrong_pw = "asdasd"
    check = check_pw_hash(wrong_pw, h)
    assert not check, "Password should be wrong"


tests = [test_1, test_2]


def _sum(a, b):
    return a + b

def test_1():
    a, b = 2, 3
    c = _sum(a, b)
    assert c == 5, "Should be 5"

def test_2():
    a, b = 2, -2
    c = _sum(a, b)
    assert c == 0, "Should be 0"

tests = [test_1, test_2]

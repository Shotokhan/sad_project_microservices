import integration_test
import time


if __name__ == "__main__":
    num_tests = len(integration_test.tests)
    start = time.time()
    for test in integration_test.tests:
        test()
    elapsed = time.time() - start
    print("{} tests executed in {} seconds".format(num_tests, elapsed))

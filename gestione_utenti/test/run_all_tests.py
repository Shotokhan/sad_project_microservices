import hash_pw_test
import utente_db_test
import paziente_db_test
import operatore_db_test


if __name__ == "__main__":
    for test in hash_pw_test.tests:
        test()
    for test in utente_db_test.tests:
        test()
    for test in paziente_db_test.tests:
        test()
    for test in operatore_db_test.tests:
        test()

def verifyCF(_codiceFiscale):
    return True


def verifyTesseraSanitaria(_tesseraSanitaria):
    return True


def verifyPaziente(paziente):
    return verifyCF(paziente.codiceFiscale) and verifyTesseraSanitaria(paziente.tesseraSanitaria)


def verifyLuogo(luogo):
    return True

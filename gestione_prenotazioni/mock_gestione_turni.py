import datetime


def verificaFinestraTemporale(etaPaziente):
    thisYear = datetime.date.today().year
    f = lambda m: datetime.date(thisYear, m, 1)
    windows = {80: f(1), 60: f(3), 40: f(5), 20: f(7), 0: f(9)}
    etaPaziente = (etaPaziente // 20) * 20
    if etaPaziente > 80:
        etaPaziente = 80
    elif etaPaziente < 0:
        etaPaziente = 0
    try:
        if datetime.date.today() >= windows[etaPaziente]:
            return True, windows[etaPaziente]
        else:
            return False, windows[etaPaziente]
    except KeyError:
        return False, f(9)

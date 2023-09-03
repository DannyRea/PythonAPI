from datetime import date as dt


def database_date(date=None):
    if not date:
        return dt.today()
    return dt.isoformat(date)

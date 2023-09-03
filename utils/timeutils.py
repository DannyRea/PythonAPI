import time as t
from datetime import datetime


def database_time(time=None):
    if not time:
        return t.strftime("%hh:%mm", t.localtime())
    return t.strftime("hh:mm", datetime.strptime(time, "%hh:%mm"))

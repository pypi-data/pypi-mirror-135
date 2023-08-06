from datetime import datetime, timezone


def _toDatetime(ts):
    """ Converts Rally API timestamps to timezone-aware (UTC) datetime """
    if not ts:
        return
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc)


def _datetimeToTimestamp(d):
    """ Converts a datetime to a Rally API timestamp """
    if not isinstance(d, datetime):
        raise TypeError('must be a datetime')

    # https://docs.python.org/3/library/datetime.html#determining-if-an-object-is-aware-or-naive
    assert d.tzinfo is not None and d.tzinfo.utcoffset(d) is not None, 'datetime must be timezone aware'

    return int(d.timestamp() * 1000)

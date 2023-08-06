# -*- coding: utf-8 -*-
"""
Helper module to send json encoded data from Python.
(the misspelling is intentional ;-)
"""
# pylint:disable=E0202
import collections
import datetime
import decimal
import json
import re

import six
from django import http
from django.db.models.query import QuerySet
import ttcal


DJANGO = True
TTCAL = True

# Call JSON.parse() if dk.jason.parse() is not available
# (the re.sub() call removes all spaces, which is currently safe).
CLIENT_PARSE_FN = re.sub(r'\s+', "", """
    function (val) {
        return (dk && dk.jason && dk.jason.parse) ?
            dk.jason.parse(val) : JSON.parse(val)
    }
""")


# Are we sending a simple value, i.e. values that don't need the double parse
# required when sending '@type:__' encoded values?
# Currently this only checks the top level of the value.
def _is_simpleval(val):
    if isinstance(val, (decimal.Decimal, six.integer_types)):
        return True
    if isinstance(val, six.string_types) and not val.startswith('@'):
        return True
    return False


class DkJSONEncoder(json.JSONEncoder):
    """Handle special cases, like Decimal...
    """

    def default(self, o):  # pylint:disable=too-many-branches,too-many-return-statements

        if isinstance(o, decimal.Decimal):
            return float(o)
        if hasattr(o, '__json__'):
            return o.__json__()
        if isinstance(o, set):
            return list(o)

        if isinstance(o, ttcal.Year):
            return dict(year=o.year, kind='YEAR')
        if isinstance(o, ttcal.Duration):
            return '@duration:%d' % o.toint()

        if isinstance(o, datetime.datetime):
            return '@datetime:%s' % o.isoformat()
        if isinstance(o, datetime.date):
            return '@date:%s' % o.isoformat()
        if isinstance(o, datetime.time):
            return dict(hour=o.hour,
                        minute=o.minute,
                        second=o.second,
                        microsecond=o.microsecond,
                        kind="TIME")

        if isinstance(o, QuerySet):
            return list(o)

        if hasattr(o, '__dict__'):
            return dict((k, v) for k, v in o.__dict__.items()
                        if not k.startswith('_'))

        if isinstance(o, collections.abc.Mapping):
            return dict(o)

        if isinstance(o, bytes):  # pragma: no branch
            return o.decode('u8')

        if isinstance(o, collections.abc.Iterable):
            return list(o)

        return super().default(o)


def dumps(val, indent=4, sort_keys=True, cls=DkJSONEncoder):
    """Dump json value, using our special encoder class.
    """
    return json.dumps(val, indent=indent, sort_keys=sort_keys, cls=cls)


def dump2(val, **kw):
    """Dump using a compact dump format.
    """
    kw['indent'] = kw.get('indent', None)
    kw['cls'] = kw.get('cls', DkJSONEncoder)
    kw['separators'] = kw.get('separators', (',', ':'))
    return json.dumps(val, **kw)


DATETIME_RE = re.compile(r'''
    @datetime:
        (?P<year>\d{4})
        -(?P<mnth>\d\d?)
        -(?P<day>\d\d?)
        T(?P<hr>\d\d?)
        :(?P<min>\d\d?)
        :(?P<sec>\d\d?)
        (?:\.(?P<ms>\d+)Z?)?
''', re.VERBOSE)


def obj_decoder(pairs):
    """Reverses values created by DkJSONEncoder.
    """

    def _get_tag(value):
        """Return the tag part of val, if it exists.
           Ie. @datetime:2021-11-15T12:15:47.1234 returns @datetime:
        """
        if isinstance(value, six.text_type) and value.startswith('@'):
            try:
                value = str(value)
            except UnicodeEncodeError:  # pragma: nocover
                return None
            else:
                if ':' not in value:
                    return None
                tag, _val = value.split(':', 1)
                return tag + ':'
        else:
            return None

    res = collections.OrderedDict()
    for key, val in pairs:
        tag = _get_tag(val)
        if tag and tag == '@datetime:':
            val = str(val)
            m = DATETIME_RE.match(val)  # pylint:disable=invalid-name
            g = m.groupdict()           # pylint:disable=invalid-name
            val = datetime.datetime(
                int(g['year']),
                int(g['mnth']),
                int(g['day']),
                int(g['hr']),
                int(g['min']),
                int(g['sec']),
                int(g.get('ms', '0') or 0)
            )
            # val = datetime.datetime.strptime(val[len('@datetime:'):],
            #                                  '%Y-%m-%dT%H:%M:%S.%f')
        elif tag and tag == '@date:':
            val = datetime.date(
                *[int(part, 10)
                  for part in val[len('@date:'):].split('-')])
        res[key] = val
    return res


def loads(txt, **kw):
    """Load json data from txt.
    """
    if 'cls' not in kw:
        kw['object_pairs_hook'] = kw.get('object_pairs_hook', obj_decoder)
    if isinstance(txt, bytes):
        txt = txt.decode('u8')
    return json.loads(txt, **kw)


def json_eval(txt):
    """Un-serialize json value.
    """
    return loads(txt)


def jsonname(val):
    """Convert the string in val to a valid json field name.
    """
    return val.replace('.', '_')


def response(request, val, **kw):
    """Return a json or jsonp response.
    """
    if request.GET.get('callback'):
        return jsonp(request.GET['callback'], val, **kw)
    return jsonval(val, **kw)


def jsonval(val, **kw):
    """Serialize val to a json HTTP response.
    """
    data = dumps(val, **kw)
    resp = http.HttpResponse(data, content_type='application/json')
    resp['Content-Type'] = 'application/json; charset=UTF-8'
    return resp


def jsonp(callback, val, **kw):
    """Serialization with json callback.
    """
    if _is_simpleval(val):
        data = callback + '(%s)' % dump2(val, **kw)
    else:
        data = callback + '(%s(%s))' % (
            CLIENT_PARSE_FN,
            dump2(dump2(val, **kw)))

    return http.HttpResponse(
        data,
        content_type='application/javascript; charset=utf-8'
    )

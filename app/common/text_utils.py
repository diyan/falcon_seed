from __future__ import unicode_literals, absolute_import, division

from base64 import b64decode, b64encode
from collections import Mapping, Iterable
import re


_all_cap_regex = re.compile('([a-z0-9])([A-Z])')


def to_underscore(value):
    if isinstance(value, Mapping):
        new_dict = {}
        _to_underscore_dict(value, new_dict)
        return new_dict
    elif (not isinstance(value, basestring)) and isinstance(value, Iterable):
        new_list = []
        _to_underscore_list(value, new_list)
        return new_list
    return _to_underscore_str(value)


def to_camel_case(value):
    if isinstance(value, Mapping):
        new_dict = {}
        _to_camel_case_dict(value, new_dict)
        return new_dict
    elif (not isinstance(value, basestring)) and isinstance(value, Iterable):
        new_list = []
        _to_camel_case_list(value, new_list)
        return new_list
    return _to_camel_case_str(value)


def to_first_lower(s):
    if s:
        return s[0].lower() + s[1:]


def base64_encode(s, altchars=None, trim_padding=False):
    encoded = b64encode(s, altchars=altchars)
    if trim_padding:
        encoded = encoded.strip('=\n')
    return encoded


def base64_decode(s, altchars=None, add_padding=False):
    to_decode = s
    if add_padding:
        to_decode = s + '=' * (4 - len(s) % 4)
    return b64decode(to_decode.encode('ascii'), altchars=altchars)


def _to_underscore_str(value):
    return _all_cap_regex.sub(r'\1_\2', value).lower().replace('__', '_')


def _to_underscore_dict(in_dict, out_dict):
    for key, value in in_dict.iteritems():
        if isinstance(value, Mapping):
            new_dict = {}
            out_dict[_to_underscore_str(key)] = new_dict
            _to_underscore_dict(value, new_dict)
        elif (not isinstance(value, basestring)) and isinstance(value, Iterable):
            new_list = []
            _to_underscore_list(list(value), new_list)
            out_dict[_to_underscore_str(key)] = new_list
        else:
            out_dict[_to_underscore_str(key)] = value


def _to_underscore_list(in_list, out_list):
    for item in in_list:
        if isinstance(item, Mapping):
            new_dict = {}
            _to_underscore_dict(item, new_dict)
            out_list.append(new_dict)
        elif (not isinstance(item, basestring)) and isinstance(item, Iterable):
            new_list = []
            _to_underscore_list(item, new_list)
            out_list.append(new_list)
        else:
            out_list.append(item)


def _to_camel_case_str(value):
    words = value.split('_')
    return words[0] + ''.join(map(unicode.capitalize, words[1:]))


def _to_camel_case_dict(in_dict, out_dict):
    for key, value in in_dict.iteritems():
        if isinstance(value, Mapping):
            new_dict = {}
            out_dict[_to_camel_case_str(key)] = new_dict
            _to_camel_case_dict(value, new_dict)
        elif (not isinstance(value, basestring)) and isinstance(value, Iterable):
            new_list = []
            _to_camel_case_list(list(value), new_list)
            out_dict[_to_camel_case_str(key)] = new_list
        else:
            out_dict[_to_camel_case_str(key)] = value


def _to_camel_case_list(in_list, out_list):
    for item in in_list:
        if isinstance(item, Mapping):
            new_dict = {}
            _to_camel_case_dict(item, new_dict)
            out_list.append(new_dict)
        elif (not isinstance(item, basestring)) and isinstance(item, Iterable):
            new_list = []
            _to_camel_case_list(item, new_list)
            out_list.append(new_list)
        else:
            out_list.append(item)
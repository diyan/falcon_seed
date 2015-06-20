from __future__ import unicode_literals
import json
from difflib import unified_diff


def _reorder(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = _reorder(v)
    if isinstance(obj, tuple):
        obj = tuple(_reorder(list(obj)))
    if isinstance(obj, list):
        obj = sorted(obj)
        for i, v in enumerate(obj):
            obj[i] = _reorder(v)
    return obj


def assert_deep_equal(first, second):
    from copy import deepcopy

    first = json.loads(first) if isinstance(first, basestring) else first
    second = json.loads(second) if isinstance(second, basestring) else second

    f = _reorder(deepcopy(first))
    s = _reorder(deepcopy(second))
    first_str = json.dumps(f, indent=4, sort_keys=True)
    second_str = json.dumps(s, indent=4, sort_keys=True)
    diff = '\n'.join(unified_diff(
        first_str.splitlines(), second_str.splitlines(), fromfile='first argument', tofile='second argument'))
    if diff:
        raise AssertionError('Payloads are not equals.\n' + diff)


def _sort_dict(ordered_dict):
    items = sorted(ordered_dict.items(), key=lambda x: x[0])
    ordered_dict.clear()
    for key, value in items:
        if isinstance(value, dict):
            _sort_dict(value)
        ordered_dict[key] = value
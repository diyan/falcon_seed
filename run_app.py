#!/usr/bin/env python
from __future__ import unicode_literals, absolute_import, division

# TODO werkzeug reloader may crash, search for more reliable solution
from werkzeug.serving import run_simple

from app import create_app

app = create_app()

if __name__ == '__main__':
    #run_simple('127.0.0.1', 5000, api, use_debugger=True, use_reloader=True)
    # Werkzeug reloader is not resilient to Python syntax error
    run_simple('127.0.0.1', 5000, app, use_reloader=True)
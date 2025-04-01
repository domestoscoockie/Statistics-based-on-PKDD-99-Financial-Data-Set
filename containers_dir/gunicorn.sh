#!/bin/bash
exec gunicorn -c ./gunicorn.conf.py 'PKDD:create_app()'

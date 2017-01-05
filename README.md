falcon portal
============

## Install dependency

    # yum install -y python-virtualenv

    $ cd /home/work/open-falcon/portal/
    $ virtualenv ./env

    # use douban pypi
    $ ./env/bin/pip install -r requirements.txt -i http://pypi.douban.com/simple


## Init database and config

- database schema: scripts/schema.sql
- database config: frame/config.py

## Start

    $ cp .env.example .env

    $ . env/bin/activate
    $ env `cat .env | xargs` python wsgi.py

    --> goto http://127.0.0.1:5050


## Run with gunicorn

    $ . env/bin/activate
    $ env `cat .env 2>/dev/null | xargs` gunicorn -c gunicorn.conf wsgi:app

    --> goto http://127.0.0.1:5050



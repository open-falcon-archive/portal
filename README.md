falcon portal
============

## install dependency

    # yum install -y python-virtualenv

    $ cd /home/work/open-falcon/portal/
    $ virtualenv ./env

    # use douban pypi
    $ ./env/bin/pip install -r pip_requirements.txt -i http://pypi.douban.com/simple


## init database and config

- database schema: scripts/schema.sql
- database config: frame/config.py

## start

    $ ./env/bin/python wsgi.py

    --> goto http://127.0.0.1:5050


## run with gunicorn

    $ . env/bin/activate
    $ bash run.sh
    
    --> goto http://127.0.0.1:5050



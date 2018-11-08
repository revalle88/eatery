from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.events import NewRequest
import os
import sqlite3
import psycopg2
import logging
import yaml


logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


# init db connection per request
@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    request.conn = db_connect()
    request.cur = request.conn.cursor()
    request.add_finished_callback(close_db_connection)


def close_db_connection(request):
    request.cur.close()
    request.conn.close()


@subscriber(ApplicationCreated)
def application_created_subscriber(event):
    log.warning('Initializing database...')
    with open(os.path.join(here, 'schema.sql')) as f:
        stmt = f.read()
        conn = db_connect()
        cur = conn.cursor()
        try:
            cur.execute(stmt)
            conn.commit()
        except psycopg2.DatabaseError as e:
            print('Error is %s' % e)
        log.warning('Database initialized...')


def db_connect():
    with open(os.path.join(here, "config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
        try:
            conn = psycopg2.connect(database=cfg['dbname'],
                                    user=cfg['user'],
                                    password=cfg['password'],
                                    host=cfg['host'])
        except psycopg2.DatabaseError as e:
            print('Error is %s' % e)
    return conn

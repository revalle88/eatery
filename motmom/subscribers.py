from pyramid.events import subscriber
from pyramid.events import ApplicationCreated
from pyramid.events import NewRequest
import os
import sqlite3
import psycopg2
import logging


logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


# init db connection per request
@subscriber(NewRequest)
def new_request_subscriber(event):
    request = event.request
    settings = request.registry.settings
    # TODO убрать настройки в файл конфигурации
    request.conn = psycopg2.connect("dbname=motmom user=postgres password=gliA6kkvn host=localhost")
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
        # TODO убрать настройки в файл конфигурации
        conn = psycopg2.connect("dbname=motmom user=postgres password=gliA6kkvn host=localhost")
        cur = conn.cursor()
        # cur.execute(stmt)
        # conn.commit()
        log.warning('statement executed...')

import os
import logging
import sqlite3
import psycopg2
import pyqrcode
import png


from pyramid.config import Configurator


from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

import os


from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from wsgiref.simple_server import make_server

from pyramid.authentication import BasicAuthAuthenticationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow, Everyone
from pyramid.security import Authenticated
from pyramid.security import (
    remember,
    forget,
    )

from .security import groupfinder, get_user_role, get_user_name


logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))



class Root(object):
    __acl__ = [(Allow, Everyone, 'view'),
               (Allow, 'developer', 'developer'),
               (Allow, 'baker','baker')]

    def __init__(self, request):
        pass


def main(global_config, **settings):
    # configuration settings
    settings = {}
    settings['reload_all'] = True
    settings['debug_all'] = True
    settings['db'] = os.path.join(here, 'motmom.db')
    settings['mako.directories'] = os.path.join(here, 'templates')
    # session factory
    session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    # configuration setup
    config = Configurator(settings=settings, session_factory=session_factory, root_factory=Root)
    # add mako templating
    config.include('pyramid_mako')
    # routes setup
    config.add_route('list', '/list')
    config.add_route('product_list', '/products')
    config.add_route('order_list', '/orders')
    config.add_route('new', '/new')
    config.add_route('create_order', '/createorder')
    config.add_route('close', '/close/{id}')
    config.add_route('add_to_order', '/toorder/{id}')
    config.add_route('cart', '/cart')
    config.add_route('register', '/register')
    config.add_route('report', '/report')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('home', '/')

    # static view setup
    config.add_static_view('static', os.path.join(here, 'static'))

    settings['auth.secret'] = 'seekrit'

    # authn_policy = BasicAuthAuthenticationPolicy(check_credentials)
    authn_policy = AuthTktAuthenticationPolicy(
        settings['auth.secret'],
        callback=groupfinder,
        hashalg='sha512',
    )
    # authn_policy = BasicAuthAuthenticationPolicy()
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    # config.set_root_factory(lambda request: Root())
    # request method get user role
    config.add_request_method(get_user_role, 'user_role', reify=True)
    # request method get username
    config.add_request_method(get_user_name, 'user_name', reify=True)

    # scan for @view_config and @subscriber decorators
    #config.scan()
    config.scan('.views')
    config.scan('.subscribers')
    return config.make_wsgi_app()
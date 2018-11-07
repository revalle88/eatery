from pyramid.response import Response
from pyramid.view import view_config
import psycopg2
from pyramid.view import forbidden_view_config
from pyramid.httpexceptions import HTTPFound
import logging
import os
import pyqrcode
import png
from pyramid.security import (
    remember,
    forget,
    )

logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


# views
@view_config(route_name='home', renderer='home.mako')
def home(request):
    return {}


@view_config(route_name='product_list', renderer='product_list.mako',
             permission='developer')
def product_list(request):
    request.cur.execute('select id, name, price from products')
    products = [dict(id=row[0], name=row[1], price=row[2])
                for row in request.cur.fetchall()]
    return {'products': products}


# add product to order
@view_config(route_name='add_to_order')
def add_to_order(request):
    bid_id = int(request.matchdict['id'])
    session = request.session
    if 'order_list' in session:
        session['order_list'].append(bid_id)
    else:
        session['order_list'] = [bid_id]
    return HTTPFound(location=request.route_url('product_list'))


@view_config(route_name='list', renderer='list.mako', permission='developer')
def list_view(request):
    request.cur.execute('select id, food, price, qrcode, comment from bids' +
                        ' where user_id=%s', (request.authenticated_userid,))
    bids = [dict(id=row[0], food=row[1], price=row[2], qrcode=row[3],
                 comment=row[4]) for row in request.cur.fetchall()]
    return {'bids': bids}


@view_config(route_name='order_list', renderer='order_list.mako',
             permission='baker')
def order_list(request):
    request.cur.execute('select b.id, b.food, b.price, b.comment, u.username' +
                        ' from bids as b INNER JOIN users as u ' +
                        'ON u.id = b.user_id')
    bids = [dict(id=row[0], food=row[1], price=row[2], comment=row[3],
            username=row[4]) for row in request.cur.fetchall()]
    return {'bids': bids}


@view_config(route_name='cart', renderer='cart.mako', permission='developer')
def cart_view(request):
    session = request.session
    message = ''
    bid_content = ''
    summ = 0
    if 'order_list' in session:
        log.warning(','.join(map(str, session['order_list'])))
        request.cur.execute("select id, name, price from products" +
                            " where id in (" +
                            ','.join(map(str, session['order_list'])) + ")")
        products = [dict(id=row[0], name=row[1], price=row[2])
                    for row in request.cur.fetchall()]
        for product in products:
            bid_content = bid_content + product['name'] + '; '
            summ = summ + product['price']
        log.warning(summ)
        return dict(
            message=message,
            bid_content=bid_content,
            summ=summ,
            products=products,
        )
    else:
        message = "empty"
        return {'empty': 'empty'}


@view_config(route_name='create_order')
def create_order(request):
    if 'form.submitted' in request.params:
        price = request.params['price']
        food = request.params['food']
        comment = request.params['comment']
        log.warning('price:  ')
        log.warning(price)
        qr = pyqrcode.create(str(price))
        request.cur.execute(
                "insert into bids (food, price, user_id, comment) " +
                "values (%s, %s, %s, %s)",
                (food, price, request.authenticated_userid, comment))
        request.conn.commit()
        request.cur.execute("select id from bids order by id DESC")
        row = request.cur.fetchone()
        bid_id = row[0]
        qrpath = 'static/qr/qr'+str(bid_id)+'.png'
        qrpathos = os.path.join(here, 'static')+'\\qr\\qr'+str(bid_id)+'.png'
        qr.png(qrpathos, scale=5)
        request.cur.execute(
            "update bids set qrcode = %s where id = %s", (qrpath, bid_id))
        request.conn.commit()
        del request.session['order_list']
        request.session.flash('New bid was successfully added!')
        return HTTPFound(location=request.route_url('list'))
    else:
            request.session.flash('Please enter a your meal list!')
    return HTTPFound(location=request.route_url('list'))


@view_config(route_name='close')
def close_view(request):
    bid_id = int(request.matchdict['id'])
    request.cur.execute("delete from bids where id = %s", (bid_id,))
    request.conn.commit()
    request.session.flash('Bid was successfully deleted!')
    return HTTPFound(location=request.route_url('list'))


@view_config(context='pyramid.exceptions.NotFound', renderer='notfound.mako')
def notfound_view(request):
    request.response.status = '404 Not Found'
    return {}


# baker views
@view_config(route_name='report', renderer='report.mako', permission='baker',)
def report_view(request):
    request.cur.execute("Select u.username, SUM(b.price) from bids b" +
                        " INNER JOIN users u ON u.id = b.user_id" +
                        " GROUP BY u.username")
    records = [dict(username=row[0], total=row[1])
               for row in request.cur.fetchall()]
    return {'records': records}


# Registration
@view_config(route_name='register', renderer='register.mako')
def register_view(request):
    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        user_role = request.params['role']
        request.cur.execute("insert into users (username, password, role) " +
                            "values (%s, %s, %s)",
                            (username, password, user_role))
        request.conn.commit()
        request.session.flash('Пользователь зарегистрирован!')
        return HTTPFound(location=request.route_url('login'))
    return {}


@view_config(route_name='login', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login(request):
    next_url = request.params.get('next', request.referrer)
    if not next_url:
        next_url = request.route_url('home')
    if next_url == request.route_url('login'):
        next_url = request.route_url('home')
    message = ''
    login = ''
    user_id = None
    if 'form.submitted' in request.params:
        username = request.params['username']
        password = request.params['password']
        request.cur.execute(
            "select id from users where username = %s and password = %s",
            (username, password,))
        if request.cur.rowcount > 0:
            rows = request.cur.fetchone()
            user_id = rows[0]
        if user_id is not None:
            log.warning('user_id:  ')
            log.warning(user_id)
            headers = remember(request, user_id)
            return HTTPFound(location=next_url,
                             headers=headers)
        message = 'Failed login'
    return dict(
        message=message,
        url=request.route_url('login'),
        next_url=next_url,
        login=login,
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    return HTTPFound(location=request.route_url('list'), headers=headers)


# @forbidden_view_config()
def forbidden_view(request):
    if request.authenticated_userid is None:
        response = HTTPUnauthorized()
        response.headers.update(forget(request))
    # user is logged in but doesn't have permissions, reject wholesale
    else:
        response = HTTPForbidden()
    return response

import psycopg2
import logging
import os
import pyqrcode
import png

logging.basicConfig()
log = logging.getLogger(__file__)
here = os.path.dirname(os.path.abspath(__file__))


def save_order(request):
    price = request.params['price']
    food = request.params['food']
    comment = request.params['comment']
    request.cur.execute(
            "insert into bids (food, price, user_id, comment) " +
            "values (%s, %s, %s, %s)",
            (food, price, request.authenticated_userid, comment))
    request.conn.commit()
    request.cur.execute("select id from bids order by id DESC")
    row = request.cur.fetchone()
    bid_id = row[0]
    qr = pyqrcode.create('order id: ' + str(bid_id) + ' price: ' + str(price))
    qrpath = 'static/qr/qr'+str(bid_id)+'.png'
    qrpathos = os.path.join(here, 'static')+'\\qr\\qr'+str(bid_id)+'.png'
    qr.png(qrpathos, scale=5)
    request.cur.execute(
        "update bids set qrcode = %s where id = %s", (qrpath, bid_id))
    request.conn.commit()


def get_user_order(order_list, cursor):
    message = ''
    bid_content = ''
    summ = 0
    cursor.execute("select id, name, price from products" +
                   " where id in (" +
                   ','.join(map(str, order_list)) + ")")
    products = [dict(id=row[0], name=row[1], price=row[2])
                for row in cursor.fetchall()]
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

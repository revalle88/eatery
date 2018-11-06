# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<%block name="page_title">
  Корзина
</%block>

% if not empty:
<h1>Ваш заказ:</h1>
% if products:


  <table class="table">
  <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Блюдо</th>
      <th scope="col">Цена</th>
    </tr>
  </thead>
  <tbody>

  % for product in products:
  <tr>
    <th scope="row">${product['id']}</th>
    <td>${product['name']}</td>
    <td>${product['price']} руб.</td>
  </tr>

  % endfor
    </tbody>
  </table>


   <div>Вы выбрали: ${bid_content}</div>
    <div>Всего к оплате: ${summ} руб.</div>
    <form action="${request.route_url('create_order')}" method="post">
      <input type="hidden" maxlength="200" name="food" value = "${bid_content}">
      <div class="form-group">
        <label for="comment">Оставьте комментарий к заказу:</label>
        <textarea rows="5" class="form-control" maxlength="200" name="comment"></textarea>
      </div>
      <input type="hidden" maxlength="200" name="price" value = "${summ}">
      <br>
      <input type="submit" class="btn btn-default" name="form.submitted" value="Подтвердить">
    </form>
    <br>
% else:
  <li>Your cart is empty</li>
% endif

</ul>

% else:
<li>Your cart is empty</li>
% endif
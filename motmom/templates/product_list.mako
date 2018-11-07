# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<%block name="page_title">
    Меню
</%block>

<h1>Наше меню:</h1>

<table class="table">
  <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Блюдо</th>
      <th scope="col">Цена</th>
      <th scope="col">добавить</th>
    </tr>
  </thead>
  <tbody>
% if products:
  % for product in products:
  <tr>
    <th scope="row">${product['id']}</th>
    <td>${product['name']}</td>
    <td>${product['price']} руб.</td>
    <td><a href="${request.route_url('add_to_cart', id=product['id'])}">Добавить в заказ</a></td>
  </tr>
  % endfor
% else:
  There are no Products
% endif

  </tbody>
</table>













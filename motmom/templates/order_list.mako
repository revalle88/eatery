# -*- coding: utf-8 -*-
<%inherit file="admin_layout.mako"/>

<%block name="page_title">
  Заказы
</%block>

<h2>Список всех заказов</h2>

<table class="table bidlist">
  <thead>
    <tr>
      <th scope="col">№</th>
      <th scope="col">Сотрудник</th>
      <th scope="col">Заказ</th>
      <th scope="col">Сумма</th>
      <th scope="col">Комментарий</th>
      <!--<th scope="col">Удалить</th>-->
    </tr>
  </thead>
  <tbody>
% if bids:
  % for bid in bids:
  <tr>
    <th scope="row">${bid['id']}</th>
    <td >${bid['username']}</td>
    <td >${bid['food']}</td>
    <td>${bid['price']} руб.</td>
    <td >${bid['comment']}</td>
    <!-- <td><a href="${request.route_url('close', id=bid['id'])}">Удалить</a></td> -->
  </tr>
  % endfor
    </tbody>
  </table>
% else:
  <li>There are no bids</li>
% endif

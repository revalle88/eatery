# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<%block name="page_title">
    Главная
</%block>

<h2>Добро пожаловать в нашу столовую!</h2>

<ul class="list-group home_list">
<li class="list-group-item">Для клиентов:</li>
  <li class="list-group-item list-group-item-success"><a href="${request.route_url('product_list')}">Меню</a></li>
  <li class="list-group-item list-group-item-primary"><a href="${request.route_url('list')}">Мои заказы</a></li>
<br><br>
<ul class="list-group home_list">
<li class="list-group-item">Для сотрудников столовой:</li>
  <li class="list-group-item list-group-item-light"><a href="${request.route_url('report')}">Отчет</a></li>
  <li class="list-group-item list-group-item-dark"><a href="${request.route_url('order_list')}">Все заказы</li>
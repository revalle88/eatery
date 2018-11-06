# -*- coding: utf-8 -*-
<%inherit file="admin_layout.mako"/>

<%block name="page_title">
  Отчет
</%block>

<h2>Сводный отчет по сотрудникам</h2>

<ul class="list-group home_list">
% if records:
  % for record in records:
  <li class="list-group-item">
    <span class="name">${record['username']}: </span>
    <span class="name">${record['total']} руб.</span>


  </li>
  % endfor
% else:
  <li>There are no records this month</li>
% endif

</ul>





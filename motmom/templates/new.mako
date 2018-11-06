# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<%block name="page_title">
    NEW
</%block>

<h1>Add a new task</h1>

<form action="${request.route_url('new')}" method="post">

  <input type="text" maxlength="200" name="food">
  <input type="submit" name="add" value="ADD" class="button">
</form>
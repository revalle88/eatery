# -*- coding: utf-8 -*-
<%inherit file="layout.mako"/>

<h1>Login:</h1>
<span>${message}</span>
<form action="${request.route_url('login')}" method="post">
  <input type="text" maxlength="100" name="username">
  <input type="password" maxlength="20" name="password">
  <input type="submit" name="form.submitted" value="Login" class="button">
</form>



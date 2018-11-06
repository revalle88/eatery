# -*- coding: utf-8 -*-
<%inherit file="admin_layout.mako"/>

<h1>Регистрация</h1>

<form action="${request.route_url('register')}" method="post">
<div class="form-group">
  <label for="username">username:</label>
  <input type="text" maxlength="100" name="username" minlength="3" required>
</div>
<div class="form-group">
    <label for="password">password:</label>
    <input type="password" maxlength="20" name="password" minlength="6" required>
</div>
<div class="form-group">
<label for="role">role:</label>
  <select name="role" size="1" required>
    <option value='developer'>разработчик</option>
    <option value='baker'>пекарь</option>
  </select>
</div>
  <input type="submit" name="form.submitted" value="Register" class="button">

</form>

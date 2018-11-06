# -*- coding: utf-8 -*-
<!DOCTYPE html>
<html>
<head>

  <meta charset="utf-8">
  <title>Pyramid Motmom</title>
  <meta name="author" content="Pylons Project">
  <link rel="shortcut icon" href="/static/favicon.ico">

  <link rel="stylesheet" href="/static/bootstrap/bootstrap.min.css">
  <link rel="stylesheet" href="/static/bootstrap/bootstrap.min.js">
  <link rel="stylesheet" href="/static/style.css">

</head>

<body>
  <div class="container">
   <div class="header clearfix">
        <nav>
         <ul class="nav nav-pills float-right">
         <li class="nav-item">
              <a class="nav-link" href="${ request.route_url('home') }">Главная</a>
            </li>
          %  if request.authenticated_userid is None:
            <li class="nav-item">
              <a class="nav-link" href="${ request.route_url('login') }">Войти</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="${ request.route_url('register') }">Зарегистрироваться</a>
            </li>
          % else:
            <li class="nav-item">
              <a class="nav-link" href="${ request.route_url('cart') }">Корзина</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="${request.route_url('logout')}">Выйти</a>
            </li>
          % endif
          </ul>
        </nav>
        <h4 class="text-muted"><%block name="page_title"/></h4>
    </div>
    <div>
    % if request.authenticated_userid:
      <div class="user_info">Вы вошли как: ${request.user_name}, роль: ${request.user_role}</div>
    % endif
    </div>
  <div class="content">




  </div>


  % if request.session.peek_flash():
  <div id="flash">
    <% flash = request.session.pop_flash() %>
	% for message in flash:
	${message}<br>
	% endfor
  </div>
  % endif

  <div id="page">

    ${next.body()}

  </div>
  </div><!-- /container -->

</body>
</html>
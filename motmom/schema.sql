CREATE TABLE products(
    id        serial PRIMARY KEY,
    name       varchar(100) NOT NULL,
    description        varchar(200),
    price        integer NOT NULL
);
ALTER TABLE products
  OWNER TO postgres;

CREATE TABLE users(
  id        serial PRIMARY KEY,
  username       varchar(100) NOT NULL,
  password       varchar(100) NOT NULL,
  role       varchar(100) NOT NULL
);
ALTER TABLE users
  OWNER TO postgres;

CREATE TABLE bids(
  id        serial PRIMARY KEY,
  user_id        integer NOT NULL,
  food        varchar(200),
  price        integer NOT NULL,
  qrcode       varchar(100),
  comment       varchar(100)
);
ALTER TABLE bids
  OWNER TO postgres;



insert into products (id, name, description, price) values (0, 'Суп Гороховый', 'descripiton', 23);
insert into products (id, name, description, price) values (1, 'Картофель', 'descripiton', 32);
insert into products (id, name, description, price) values (2, 'Хлеб', 'descripiton', 7);
insert into products (id, name, description, price) values (3, 'Чай', 'descripiton', 12);
insert into products (id, name, description, price) values (4, 'Компот', 'descripiton', 15);

/*
insert into users (id, username, password, role) values (0, 'baker', 'baker', 'baker');
insert into users (id, username, password, role) values (1, 'developer', 'developer', 'developer');
insert into users (id, username, password, role) values (2, 'hello', 'world', 'developer');*/
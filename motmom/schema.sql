/*CREATE TABLE products(
    id        serial PRIMARY KEY,
    name       varchar(100) NOT NULL,
    description        varchar(200)
);

CREATE TABLE public.products
(
  id integer NOT NULL DEFAULT nextval('products_id_seq'::regclass),
  name character varying(100) NOT NULL,
  description character varying(200),
  CONSTRAINT products_pkey PRIMARY KEY (id)
)

insert into products (id, name, description) values (0, 'Bread', 'descripiton');
insert into products (id, name, description) values (1, 'Butter', 'descri2');
insert into products (id, name, description) values (2, 'Cookie', 'descr3');

	*/

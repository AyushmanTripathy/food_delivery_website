PRAGMA foreign_keys = ON;

drop table users;
drop table items;
drop table orders;

create table users (
  id integer primary key autoincrement,
  username varchar(255) not null,
  email varchar(255) unique not null,
  address varchar(255) not null,
  password_hash varchar(255) not null
);

create table items (
  id integer primary key autoincrement,
  name varchar(255) not null,
  price int not null,
  category varchar(50) not null
);

create table orders (
  id integer primary key autoincrement,
  user_id integer,
  item_id integer,
  foreign key (item_id) references items(id),
  foreign key (user_id) references users(id)
);

insert into items (name, price, category) values 
  ('Chicken Briyani', 120, 'non veg'),
  ('Chicken Roll', 50, 'non veg'),
  ('Paneer Roll', 40, 'veg'),
  ('Egg Roll', 30, 'non veg'),
  ('Mutton Briyani', 1000000, 'non veg')
;

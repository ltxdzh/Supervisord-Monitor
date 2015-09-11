--drop table if exists entries;

create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

insert into users (username, password) values ("admin", "123");

create table servers (
  id integer primary key autoincrement,
  server_ip text not null,
  server_port text not null,
  server_name text,
  auth_user text,
  auth_pwd	text
);

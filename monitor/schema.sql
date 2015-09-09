--drop table if exists entries;

create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null
);

insert into users (username, password) values ("admin", "123");

create table hosts (
  id integer primary key autoincrement,
  host_ip text not null,
  host_name text not null,
  auth_user text,
  auth_pwd	text
);

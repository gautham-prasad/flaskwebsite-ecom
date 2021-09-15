-- create table if not exists tempusers(
-- 	id serial primary key,
-- 	email varchar(256) unique not null,
-- 	username varchar(100) unique not null,
-- 	password text not null
-- );

-- create table if not exists users(
-- 	id serial primary key,
-- 	email varchar(256) unique not null,
-- 	username varchar(100) unique not null
-- );

-- create table if not exists usersinfo(
-- 	id serial primary key,
-- 	user_id integer,
-- 	password text not null,
-- 	foreign key user_id references users(id)
-- );

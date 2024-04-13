create table roles(
id integer not null generated by default as identity,
role_name varchar(100) not null,
description varchar(255) default '',
primary key(id)
);

create table users(
id integer not null generated by default as identity,
fullname varchar(255) not null,
username varchar(30) not null,
pass varchar(1000) not null,
role_id integer not null references roles(id),
primary key(id)
);


create table videos(
id integer not null generated by default as identity,
description varchar(255) default '',
path varchar(500) not null,
user_id integer not null references users(id)
);
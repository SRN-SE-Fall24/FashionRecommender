drop database if exists fashion;
create database fashion;
use fashion;

drop table if exists user;
drop table if exists user_details;
drop table if exists preference;
drop table if exists recommendation;

create table user(
    id int not null primary key AUTO_INCREMENT,
    email varchar(255) not null unique,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    gender varchar(255) not null,
    phone_number varchar(255) not null unique,
    password varchar(255) not null,
    age int,
    city varchar(255) not null
);
create table preference (
    userid int  not null,
    preferences longtext not null,
    primary key (userid),
    foreign key (userid) references user(id));

create table recommendation (
    userid int not null,
    links json not null,
    primary key (userid),
    foreign key (userid) references user(id));

create table favourite (
    id int not null primary key AUTO_INCREMENT,
    userid int not null,
    favourite_url varchar(255) not null,
    search_occasion varchar(255) not null,
    search_weather varchar(255) not null,
    foreign key (userid) references user(id));



drop database if exists fashion_test;
create database fashion_test;
use fashion_test;

drop table if exists user;
drop table if exists user_details;
drop table if exists preference;
drop table if exists recommendation;

create table user(
    id int not null primary key AUTO_INCREMENT,
    email varchar(255) not null unique,
    first_name varchar(255) not null,
    last_name varchar(255) not null,
    gender varchar(255) not null,
    phone_number varchar(255) not null unique,
    password varchar(255) not null,
    age int,
    city varchar(255) not null
);
create table preference (
    userid int  not null,
    preferences longtext not null,
    primary key (userid),
    foreign key (userid) references user(id));

create table recommendation (
    userid int not null,
    links json not null,
    primary key (userid),
    foreign key (userid) references user(id));
    
use fashion;
select * from favourite;
truncate table favourite;
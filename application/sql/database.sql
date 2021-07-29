drop table if exists todo_list;
drop table if exists user_details; -- Storing log in Information

create table user_details (
       id SERIAL PRIMARY KEY,
       username text UNIQUE NOT NULL,
       password text NOT NULL
       );

create table todo_list (
       id SERIAL PRIMARY KEY,
       task text NOT NULL,
       date_added date not null default current_date,
       due_date date not null,
       username text,
       progress text,
       user_id int default 0
       );

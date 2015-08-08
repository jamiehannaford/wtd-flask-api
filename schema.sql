drop table if exists cats;
create table cats (
  id integer primary key autoincrement,
  name text not null,
  breed text not null,
  colour text not null,
  tail_length integer not null
);

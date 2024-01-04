create table domena(
id int not null primary key auto_increment,
uuid char(36),
naziv varchar(255) not null,
stvarnadomena varchar(255),
status int not null default 0,
datumpocetka datetime,
datumkraja datetime
);

create table stvarnadomena(
id int not null primary key auto_increment,
uuid char(36),
naziv varchar(255) not null,
status int not null default 0,
datumpocetka datetime,
datumkraja datetime
);

alter table stvarnadomena add column analiziranopoveznica int;

create table poddomena(
id int not null primary key auto_increment,
domena int not null,
naziv varchar(255) not null,
stvarnadomena varchar(255)
);

alter table poddomena add foreign key (domena) references stvarnadomena(id);

insert into stvarnadomena values
select distinct stvarnadomena from domena where status=2 and stvarnadomena is not null;
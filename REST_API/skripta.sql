create table domena(
id int not null primary key auto_increment,
uuid char(36),
naziv varchar(255) not null,
stvarnadomena varchar(255),
status int not null default 0,
datumpocetka datetime,
datumkraja datetime
);


create table poddomena(
id int not null primary key auto_increment,
domena int not null,
url varchar(255) not null
);

alter table poddomena add foreign key (domena) references domena(id);
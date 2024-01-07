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
datumkraja datetime,
sekundi int,
racunalo varchar(355)
);

insert into stvarnadomena values
select distinct stvarnadomena from domena where status=2 and stvarnadomena is not null;


create table domena_stvarnadomena(
domena int not null,
stvarnadomena int not null
);

alter table domena_stvarnadomena add foreign key (domena) references domena(id);
alter table domena_stvarnadomena add foreign key (stvarnadomena) references stvarnadomena(id);




drop table svedomene;
drop table poveznica;
drop table poddomena;

create table poddomena(
id int not null primary key auto_increment,
domena int not null,
naziv varchar(255) not null
);

alter table poddomena add foreign key (domena) references stvarnadomena(id);

create table poveznica(
id int not null primary key auto_increment,
domena int not null,
url varchar(255) not null,
dugiurl text
);

alter table poveznica add foreign key (domena) references stvarnadomena(id);

create table svedomene(
id int not null primary key auto_increment,
domena int not null,
url varchar(255) not null
);

alter table svedomene add foreign key (domena) references stvarnadomena(id);



# reset onih koji nisu završili pri traženju poddomena
update stvarnadomena set uuid=null, status=0, datumpocetka=null, datumkraja=null, sekundi=null, racunalo=null where status=1;

update stvarnadomena set uuid=null, status=0, datumpocetka=null, datumkraja=null, sekundi=null, racunalo=null where id=51445;

update stvarnadomena set uuid=null, status=0, datumpocetka=null, datumkraja=null, sekundi=null, racunalo=null where status=2 and datumpocetka is null;

# na čemu nije našao niti jednu poveznicu - vidjeti zašto nije našao i ako treba ponovo
select a.naziv from stvarnadomena a left join poveznica b on a.id=b.domena where b.domena is null and a.status=2;

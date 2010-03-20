create table accounts(numb 	integer not null, branchnum integer not null, balance float not null);
create unique index hest on accounts ( numb )  cluster PCTFREE 20;
--alter table accounts add primary key ( numb );


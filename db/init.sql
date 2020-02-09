create user concierge_dev password 'simplepass';

create database concierge_db encoding 'utf-8';
grant all privileges on database concierge_db to concierge_dev;
alter database concierge_db owner to concierge_dev;

create database concierge_test_db encoding 'utf-8';
grant all privileges on database concierge_test_db to concierge_dev;
alter database concierge_test_db owner to concierge_dev;


-- update table preferences schema
-- create new schema
create table new_preferences(
        key_ varchar(255) unique primary key not null,
        value_ varchar(65535)
);
-- transfer data
INSERT INTO new_preferences SELECT * FROM preferences;
-- delete old table
drop table preferences;
-- rename new schema
ALTER TABLE new_preferences RENAME TO preferences;

-- new preferences fields
INSERT INTO preferences (key_, value_) VALUES ("wallet_load_default_directory", null);
INSERT INTO preferences (key_, value_) VALUES ("wallet_save_default_directory", null);


-- update table preferences schema
-- create new schema
create table new_preferences(
        key_ varchar(255) unique primary key not null,
        value_ varchar(255)
);
-- transfer data
INSERT INTO new_preferences SELECT * FROM preferences;
-- delete old table
drop table preferences;
-- rename new schema
ALTER TABLE new_preferences RENAME TO preferences;

-- remove new preferences fields
DELETE FROM preferences WHERE key_ = "wallet_load_default_directory";
DELETE FROM preferences WHERE key_ = "wallet_save_default_directory";

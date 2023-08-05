create table if not exists accounts(
        pubkey varchar(255) unique primary key not null,
        uid varchar(255),
        selected boolean default 1,
        access_type varchar(8) default null
);

create table if not exists tabs(
        id varchar(255) unique primary key not null,
        panel_class varchar(255) not null
);

create table if not exists preferences(
        key_ varchar(255) unique primary key not null,
        value_ varchar(255)
);

-- PREFERENCES FIELDS
INSERT INTO preferences (key_, value_) VALUES ("selected_tab_page", NULL)

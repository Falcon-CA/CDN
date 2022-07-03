CREATE TABLE IF NOT EXISTS files (
    id      varchar(10) not null,
    name    varchar(70) not null,
    dir     varchar(10),
    type    varchar(10),
    size    bigint unsigned not null,
    created datetime not null,
    private tinyint not null,

    unique      (id),
    primary key (id)
);


CREATE TABLE IF NOT EXISTS directories (
    id      varchar(10) not null,
    name    varchar(70) not null,
    dir     varchar(10),
    created datetime not null,
    private tinyint not null,

    unique      (id),
    primary key (id)
);


CREATE TABLE IF NOT EXISTS tokens (
    token     varchar(45) not null,
    issued_at datetime not null,
    exp_sec   bigint,

    access_file_p tinyint not null,
    access_dir_p  tinyint not null,
    create_file   tinyint not null,
    create_file_p tinyint not null,
    create_dir    tinyint not null,
    create_dir_p  tinyint not null,
    delete_file   tinyint not null,
    delete_dir    tinyint not null,
    admin         tinyint not null,
    max_file_size bigint unsigned,

    unique      (token),
    primary key (token)
);
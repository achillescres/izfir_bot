create table qu_an_callback
(
    id          serial      not null,
    qu          text        not null,
    an          text        not null,
    callback    text        not null
);

alter table qu_an_callback
    owner to super;

create unique index qu_an_callback_id_uindex
    on users (id);

CREATE TABLE audit.aud (
   id SERIAL8
  ,tran_id BIGINT
  ,action character(1)
  ,tbl_id varchar(64)
  ,tbl_key varchar(128)
  ,par_tbl_id varchar(64)
  ,par_tbl_key varchar(128)
);
ALTER TABLE audit.aud ADD PRIMARY KEY (
   id
);
CREATE TABLE audit.cfg (
   id varchar(64)
  ,col_pk varchar(1024)
  ,col_ignr varchar(4096)
  ,par_id varchar(64)
  ,par_col varchar(1024)
  ,last_chg TIMESTAMP
);
ALTER TABLE audit.cfg ADD PRIMARY KEY (
   id
);
CREATE TABLE audit.tran (
   id SERIAL8
  ,site_id INTEGER
  ,who varchar(128)
  ,src varchar(128)
  ,tm_stamp TIMESTAMP
);
ALTER TABLE audit.tran ADD PRIMARY KEY (
   id
);
CREATE TABLE audit.col (
   aud_id BIGINT
  ,name varchar(64)
  ,BEFORE varchar(128)
  ,AFTER varchar(128)
);
ALTER TABLE audit.col ADD PRIMARY KEY (
   aud_id
  ,name
);
ALTER TABLE audit.tran
   ALTER COLUMN id SET NOT NULL
  ,ALTER COLUMN site_id SET NOT NULL
  ,ALTER COLUMN who SET NOT NULL
  ,ALTER COLUMN src SET NOT NULL
  ,ALTER COLUMN tm_stamp SET NOT NULL
;
ALTER TABLE audit.cfg
   ALTER COLUMN id SET NOT NULL
;
ALTER TABLE audit.cfg ADD CONSTRAINT cfg_fk_cfg FOREIGN KEY (par_id) REFERENCES audit.cfg;
ALTER TABLE audit.col
   ALTER COLUMN aud_id SET NOT NULL
  ,ALTER COLUMN name SET NOT NULL
;
ALTER TABLE audit.col ADD CONSTRAINT col_fk_aud FOREIGN KEY (aud_id) REFERENCES audit.aud;
ALTER TABLE audit.aud
   ALTER COLUMN id SET NOT NULL
  ,ALTER COLUMN tran_id SET NOT NULL
  ,ALTER COLUMN action SET NOT NULL
  ,ALTER COLUMN tbl_id SET NOT NULL
  ,ALTER COLUMN tbl_key SET NOT NULL
;
ALTER TABLE audit.aud ADD CONSTRAINT aud_fk_tran FOREIGN KEY (tran_id) REFERENCES audit.tran;
CREATE INDEX cfg_ix_par ON audit.cfg
(
   par_id
);
CREATE INDEX cfg_ix_lc ON audit.cfg
(
   id
  ,last_chg
);
CREATE INDEX aud_ix_tran ON audit.aud
(
   tran_id
);
CREATE INDEX col_uk_aud ON audit.col
(
   aud_id
);

ALTER TABLE customer
  MODIFY address_1 VARCHAR(50) NOT NULL;

ALTER TABLE customer
  MODIFY address_2 VARCHAR(50) DEFAULT '' NOT NULL;

ALTER TABLE customer
  MODIFY address_3 VARCHAR(50) DEFAULT '' NOT NULL;

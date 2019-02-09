CREATE TABLE customer
(
  id         INT AUTO_INCREMENT,
  email      VARCHAR(50) NOT NULL,
  phone      VARCHAR(13) NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  last_name  VARCHAR(20) NOT NULL,
  address_1  VARCHAR(20) NOT NULL,
  address_2  VARCHAR(20) NOT NULL,
  address_3  VARCHAR(20) NOT NULL,
  city       VARCHAR(20) NOT NULL,
  postcode   VARCHAR(7)  NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY (email)
);

CREATE TABLE `order`
(
  id                INT AUTO_INCREMENT,
  customer_id       INT NOT NULL,
  total_price_pence INT NOT NULL,
  PRIMARY KEY (id),
  INDEX customer_id_index (customer_id),
  FOREIGN KEY (customer_id) REFERENCES customer (id)
);

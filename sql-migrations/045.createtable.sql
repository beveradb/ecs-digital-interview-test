CREATE TABLE object
(
  id          INT AUTO_INCREMENT,
  name        VARCHAR(20) NOT NULL,
  type        VARCHAR(10) NOT NULL,
  description TEXT        NULL,
  PRIMARY KEY (id)
);

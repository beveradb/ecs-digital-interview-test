CREATE TABLE room
(
  id          INT AUTO_INCREMENT,
  name        VARCHAR(20) NOT NULL,
  type        VARCHAR(10) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO room (name, type)
VALUES ('Living Room', 'general'),
       ('Kitchen', 'dining'),
       ('Dining Room', 'dining'),
       ('Hallway', 'general'),
       ('Master Bedroom', 'rest'),
       ('Guest Bedroom', 'rest'),
       ('Conservatory', 'general');
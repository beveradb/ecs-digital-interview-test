ALTER TABLE item
  ADD room INT NOT NULL AFTER type;

ALTER TABLE item
  ADD CONSTRAINT item_room_id_fk
    FOREIGN KEY (room) REFERENCES room (id);

UPDATE item
SET room = (SELECT id AS room FROM room WHERE room.name = 'Dining Room')
WHERE item.name IN ('Chair', 'Table');

UPDATE item
SET room = (SELECT id AS room FROM room WHERE room.name = 'Kitchen')
WHERE item.name IN ('Knife', 'Fork');

UPDATE item
SET room = (SELECT id AS room FROM room WHERE room.name = 'Master Bedroom')
WHERE item.name IN ('Bed');



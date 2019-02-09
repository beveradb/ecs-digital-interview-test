INSERT INTO customer (email, phone, first_name, last_name, address_1,
                      city, postcode)
  VALUE ('andrew@beveridge.uk', '07835171222', 'Andrew', 'Beveridge',
         '17 Coltbridge Millside', 'Edinburgh', 'EH126AP');

INSERT INTO `order` (customer_id, total_price_pence)
  VALUE (
         (SELECT id FROM customer WHERE email = 'andrew@beveridge.uk'),
         32900
  );
DROP TABLE IF EXISTS milkchoc;

CREATE TABLE milkchoc
(
    milk_choc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);

DROP TABLE IF EXISTS whitechoc;

CREATE TABLE whitechoc
(
    white_choc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);

DROP TABLE IF EXISTS darkchoc;

CREATE TABLE darkchoc
(
    dark_choc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    description TEXT
);

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    admin_user BOOLEAN NOT NULL,
    password TEXT NOT NULL
);

INSERT INTO users (user_name, admin_user, password)
VALUES
('Amie', FALSE, 'amie'),

DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
    vote_id INTEGER PRIMARY KEY AUTOINCREMENT,
    chocolate TEXT NOT NULL,
    vote_count INTEGER NOT NULL
);


INSERT INTO votes (chocolate, vote_count) 
VALUES
('Milk', 0),
('Dark', 0),
('White', 0);

INSERT INTO milkchoc (name, price, description)
VALUES
('Plain..ish Milk Chocolate', 3.00, 'Our signature plain, old reliable, milk chocolate! Made with our own recipe.'),
('Minty Milk Heaven', 3.50, 'Minty milk chocolate, its heavenly!'),
('Honeycomb Honey', 3.50, 'Too sweet to resist!'),
('Milk Crisp', 3.50, 'Our signature milk chocolate with a crispy twist.'),
('Larger than Life - Milk', 5.00, 'Our signature milk chocolate, doubled in size.'),
('Classic Hot Choccy', 4.00, 'Stir these flakes into your favourite milk for a cup of heaven!');

INSERT INTO whitechoc (name, price, description)
VALUES
('Plain..ish White chocolate', 3.00, 'Our signature chocolate, but in white!'),
('Mixed Up..Milk', 3.50, 'Milk and white chocolate mixed to marbled perfection.'),
('Strawberry White ', 3.50, 'Fruity and delicious!'),
('Larger than Life - White', 5.00, 'Our signature white chocolate, doubled in size.'),
('White Hot Choccy', 4.00, 'Our delicious hot chocolate flakes, but in white.');;

INSERT INTO darkchoc (name, price, description)
VALUES
('Plain..ish Dark Chocolate', 3.00, 'Our signature chocolate, but dark!'),
('Deliciously dark', 3.50, 'Its healthy, right?'),
('Mixed Up.. Dark', 3.50, 'The perfect mix of dark and milk chocolate.'),
('Cookie Crumble', 3.50, 'Our signature dark chocolate with a cookie twist.'),
('Larger than Life - Dark', 5.00, 'Our signature dark chocolate, doubled in size.'),
('Dark Hot Choccy', 4.00, 'Our delicious hot chocolate flakes, but in dark.');

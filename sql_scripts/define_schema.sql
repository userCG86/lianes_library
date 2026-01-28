/********* Schema layout notes

Books - title, author, genre, id
	keys: id
    
Friends - name, max_loans, notes, id
	keys: id
    
Loans - book_id, friend_id, loan_date, last_contact, next_contact, notes
	keys: composite book_id/friend_id? auto_id?
**********/

DROP SCHEMA IF EXISTS sample_library;
CREATE SCHEMA sample_library;
USE sample_library;

DROP TABLE IF EXISTS books;
CREATE TABLE books (
	title VARCHAR(80) NOT NULL,
    author VARCHAR(80),
    genre VARCHAR(20),
    isbn VARCHAR(13) PRIMARY KEY
);

DROP TABLE IF EXISTS friends;
CREATE TABLE friends (
	friend_id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(80),
    max_loans INT DEFAULT 2,
    notes TEXT
);

DROP TABLE IF EXISTS loans;
CREATE TABLE loans (
	isbn VARCHAR(13),
    friend_id INT,
    loan_date DATE DEFAULT (CURRENT_DATE()) NOT NULL,
    last_contact DATE,
    next_contact DATE DEFAULT (DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY)),
    notes TEXT,
    FOREIGN KEY (isbn) REFERENCES books(isbn) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (friend_id) REFERENCES friends(friend_id) ON DELETE CASCADE,
    PRIMARY KEY (isbn, friend_id)
);
/**** practice statements
INSERT INTO books (title, author, genre, isbn)
VALUES ('Book One', 'Pencil Jones', 'boring', '0000000000'),
('Book Two', 'Marker Jones', 'exciting', '0000000001');

UPDATE books
SET genre = 'factual'
WHERE isbn = '0000000000';

DELETE FROM books
WHERE isbn = '0000000001';
****/

-- Insert friends
INSERT INTO friends (`name`, max_loans) VALUES
('Ellie Martinez', 2),
('Davey', 3),
('Luca Schmidt', 1),
('Amira Jansen', 2),
('Fix Bauer', 3),
('Soso Klein', 1);
UPDATE friends SET notes = 'Gets recommendations from Ellie' WHERE friend_id = 2;
UPDATE friends SET notes = 'Always takes long loans' WHERE friend_id = 3;


-- Insert books
INSERT INTO books (title, author, genre, ISBN) VALUES
('The Paper Trail', 'Liane Forestier', 'Historical Fiction', '9781234567890'),
('Echoes of the Past', 'Julian Marsh', 'Thriller', '9780987654321'),
('The Secret Ingredient', 'Samira Nouri', 'Romance', '9781122334455'),
('The Clockmaker\'s Son', 'Hugo Vernier', 'Steampunk', '9784455667788'),
('Gardens of Glass', 'Ivy Thornton', 'Fantasy', '9785566778899');


-- Insert loans
INSERT INTO loans (ISBN, friend_id, loan_date, last_contact, next_contact) VALUES
('9781234567890', 1, '2025-06-15', '2025-06-15', '2025-07-15'),
('9781122334455', 3, '2025-03-12', '2025-06-20', '2025-07-10'),
('9784455667788', 4, '2025-07-01', '2025-06-30', '2025-07-30'),
('9780987654321', 5, '2025-07-02', '2025-07-02', '2025-07-25');
UPDATE loans SET notes='Promised to return after summer holidays.' WHERE isbn = '9781122334455' AND friend_id = 3;

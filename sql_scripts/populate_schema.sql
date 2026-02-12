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

USE sample_library;

-- Clear tables before population
DELETE FROM loans;
DELETE FROM books;
DELETE FROM friends;
ALTER TABLE friends AUTO_INCREMENT = 1;

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
('Gardens of Glass', 'Ivy Thornton', 'Fantasy', '9785566778899'),
('The Wind-Up Bird Chronicle', 'Haruki Murakami', 'Fiction', '9780307949486'),
('The Alchemist', 'Paulo Coelho', 'Fiction', '9780062316110'),
('Sapiens: A Brief History of Humankind', 'Yuval Noah Harari', 'Nonfiction', '9780143127741'),
('Thinking, Fast and Slow', 'Daniel Kahneman', 'Psychology', '9780553386790'),
('The Poisonwood Bible', 'Barbara Kingsolver', 'Fiction', '9780385490818');


-- Insert loans
INSERT INTO loans (ISBN, friend_id, loan_date, last_contact, next_contact) VALUES
('9781234567890', 1, '2025-06-15', '2025-06-15', '2025-07-15'),
('9781122334455', 3, '2025-03-12', '2025-06-20', '2025-07-10'),
('9784455667788', 4, '2025-07-01', '2025-06-30', '2025-07-30'),
('9780987654321', 5, '2025-07-02', '2025-07-02', '2025-07-25');
UPDATE loans SET notes='Promised to return after summer holidays.' WHERE isbn = '9781122334455' AND friend_id = 3;

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

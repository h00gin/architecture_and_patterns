PRAGMA foreign_keys = on;
BEGIN TRANSACTION;


DROP TABLE IF EXISTS students;
CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR(32),
surname VARCHAR(32), telephone VARCHAR(32), email VARCHAR(32));
INSERT INTO students (id, name, surname, telephone, email) VALUES (1, 'Ivan', 'Ivanov', '784578', '1@gmail.com');
INSERT INTO students (id, name, surname, telephone, email) VALUES (2, 'Petr', 'Petrov', '794678', '2@gmail.com');
INSERT INTO students (id, name, surname, telephone, email) VALUES (3, 'Denis', 'Denisov', '804678', '3@gmail.com');

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR(32), category VARCHAR(32));
INSERT INTO categories (id, name, category) VALUES (1, 'Programming', '0');
INSERT INTO categories (id, name, category) VALUES (2, 'Management', '0');
INSERT INTO categories (id, name, category) VALUES (3, 'Web', '0');

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR(32),
category_id INTEGER NOT NULL, FOREIGN KEY (category_id) REFERENCES categories(id));
INSERT INTO courses (id, name, category_id) VALUES (1, 'Python', 1);
INSERT INTO courses (id, name, category_id) VALUES (2, 'Java', 1);
INSERT INTO courses (id, name, category_id) VALUES (3, 'PHP', 1);




--DROP TABLE IF EXISTS student_courses;
--CREATE TABLE student_courses (students_id INTEGER NOT NULL, courses_id INTEGER NOT NULL,
--FOREIGN KEY (students_id) REFERENCES students(id), FOREIGN KEY (courses_id) REFERENCES courses(id));
--INSERT INTO student_courses (students_id, courses_id) VALUES (1, 1);
--INSERT INTO student_courses (students_id, courses_id) VALUES (1, 2);
--INSERT INTO student_courses (students_id, courses_id) VALUES (2, 2);
--INSERT INTO student_courses (students_id, courses_id) VALUES (2, 3);
--INSERT INTO student_courses (students_id, courses_id) VALUES (3, 1);
--INSERT INTO student_courses (students_id, courses_id) VALUES (3, 3);

COMMIT TRANSACTION;




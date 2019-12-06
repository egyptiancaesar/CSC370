#!/usr/bin/python
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters and connect to postgreSQL server. Also
        # create a server and query the database for its current version.
        params = config()
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        print('Connected')
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        #sql commands:

        init_sql_lines = """
        DROP TABLE IF EXISTS Worksheet CASCADE;
    DROP TABLE IF EXISTS Volunteer CASCADE;
    DROP TABLE IF EXISTS Student CASCADE;
    DROP TABLE IF EXISTS Student_Current_Worksheet;
    DROP TABLE IF EXISTS Student_Submitted_Worksheet;
    DROP TABLE IF EXISTS Volunteer_Grading_Worksheet;
DROP TABLE IF EXISTS Graded_Worksheet;
DROP TABLE IF EXISTS Recommended_Worksheet;
DROP SEQUENCE IF EXISTS W_serial;
DROP SEQUENCE IF EXISTS V_serial;
DROP SEQUENCE IF EXISTS S_serial;
DROP SEQUENCE IF EXISTS SUB_serial;
DROP SEQUENCE IF EXISTS GRDS_serial;
DROP SEQUENCE IF EXISTS RCMND_serial;
    CREATE SEQUENCE W_serial start 1 increment 1;
CREATE SEQUENCE V_serial start 1 increment 1;
CREATE SEQUENCE S_serial start 1 increment 1;
CREATE SEQUENCE SUB_serial start 1 increment 1;
CREATE SEQUENCE GRDS_serial start 1 increment 1;
CREATE SEQUENCE RCMND_serial start 1 increment 1;

CREATE TABLE Volunteer (V_ID serial PRIMARY KEY, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, language VARCHAR(255) );

CREATE TABLE Worksheet(W_ID serial PRIMARY KEY, V_ID INT REFERENCES Volunteer, Concept VARCHAR(255), Level VARCHAR(255) NOT NULL);

CREATE TABLE Student (S_ID serial PRIMARY KEY, first_name VARCHAR(255) NOT NULL, last_name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, level VARCHAR(255) NOT NULL, school_grade VARCHAR(255)  NOT NULL, Country VARCHAR(255) NOT NULL, language VARCHAR(255), Olympiad BOOLEAN);

CREATE TABLE Student_Current_Worksheet (S_ID INT REFERENCES student, W_ID INT REFERENCES worksheet, PRIMARY KEY (s_id));

CREATE TABLE Student_Submitted_Worksheet(SUB_ID serial PRIMARY KEY, S_ID INT, W_ID INT, date date);

CREATE TABLE Volunteer_Grading_worksheet(SUB_ID INT PRIMARY KEY, V_ID INT NOT NULL, W_ID INT NOT NULL, S_ID INT NOT NULL, date date);

CREATE TABLE Graded_Worksheet(GRDS_ID serial PRIMARY KEY, S_ID INT NOT NULL, W_ID INT NOT NULL, V_ID INT NOT NULL, Language VARCHAR(255), Grade INT NOT NULL, Review VARCHAR(255));

CREATE TABLE Recommended_Worksheet(RCMND_ID serial PRIMARY KEY, S_ID INT NOT NULL, W_ID INT NOT NULL, V_ID INT NOT NULL);

INSERT INTO VOLUNTEER(v_id,first_name,last_name,email,language)
VALUES(nextval('v_serial'),'Amal','Misbah','amisbah@york.ca','English');

INSERT INTO VOLUNTEER(v_id,first_name,last_name,email,language)
VALUES(nextval('v_serial'),'Nirmala','King','nirma@uvic.ca','English');

INSERT INTO VOLUNTEER(v_id,first_name,last_name,email,language)
VALUES(nextval('v_serial'),'Jamie','Fox','jamie.fox@ubc.ca','French');

INSERT INTO WORKSHEET(w_id,v_id,concept,level)
VALUES(nextval('w_serial'), (SELECT v_id FROM volunteer WHERE first_name = 'Amal' AND last_name = 'Misbah'), 'Alegbra', '12');

INSERT INTO WORKSHEET(w_id, v_id, concept, level)
VALUES(nextval('w_serial'), (SELECT v_id FROM volunteer WHERE first_name = 'Amal' AND last_name = 'Misbah') , 'Algebra', 'College');

INSERT INTO WORKSHEET(w_id,v_id,concept,level)
VALUES(nextval('w_serial'),(SELECT v_id FROM volunteer WHERE first_name='Amal' AND last_name='Misbah'), 'Linear Algebra', 'College');

INSERT INTO WORKSHEET(w_id,v_id,concept,level)
VALUES(nextval('w_serial'),(SELECT v_id FROM volunteer WHERE first_name='Nirmala' AND last_name='King'), 'Counting' ,'3');

INSERT INTO WORKSHEET(w_id,v_id,concept,level)
VALUES(nextval('w_serial'),(SELECT v_id FROM volunteer WHERE first_name='Nirmala' AND last_name='King'), 'Adding' , '3');

INSERT INTO WORKSHEET(w_id,v_id,concept,level)
VALUES(nextval('w_serial'),(SELECT v_id FROM volunteer WHERE first_name='Jamie' AND last_name='Fox'),'Division','5');

INSERT INTO WORKSHEET(w_id,v_id,concept,level)
VALUES(nextval('w_serial'),(SELECT v_id FROM volunteer WHERE first_name='Jamie' AND last_name='Fox'),'Linear Graphs', '9');

INSERT INTO STUDENT(s_id, first_name, last_name, email, level, school_grade, country, language, olympiad)
VALUES(nextval('s_serial'), 'Omar', 'AbdulAziz',  'omarabdu@uvic.ca' , 'college', 'College' ,'Canada', 'English', TRUE);


INSERT INTO STUDENT(s_id, first_name, last_name, email, level, school_grade, country, language, olympiad)
VALUES(nextval('s_serial'), 'Ari', 'Raeyal', 'areayal@gmail.com','5','7','USA','English',FALSE);


INSERT INTO STUDENT(s_id, first_name, last_name, email, level, school_grade, country, language, olympiad)
VALUES(nextval('s_serial'), 'Sam', 'Manny', 'samman@hotmail.com','9','7','France','French',FALSE);


SELECT * FROM volunteer;
SELECT * FROM worksheet;
SELECT * FROM student;

INSERT INTO STUDENT_CURRENT_WORKSHEET(s_id, w_id)
VALUES((SELECT s_id FROM student WHERE first_name='Omar' AND last_name='AbdulAziz'), 3);

INSERT INTO STUDENT_CURRENT_WORKSHEET(s_id,w_id)
VALUES((SELECT s_id FROM student WHERE first_name='Ari' AND last_name='Raeyal'),6);

INSERT INTO STUDENT_CURRENT_WORKSHEET(s_id,w_id)
VALUES((SELECT s_id FROM student WHERE first_name='Sam' AND last_name='Manny'),7);

BEGIN;
	INSERT INTO STUDENT_SUBMITTED_WORKSHEET(sub_id, s_id,w_id,date) 
	VALUES(nextval('sub_serial'), 1, 2, CURRENT_DATE);
	UPDATE STUDENT_CURRENT_WORKSHEET SET w_id = 3 WHERE s_id =1;
COMMIT;

BEGIN;
	INSERT INTO STUDENT_SUBMITTED_WORKSHEET(sub_id,s_id,w_id,date)
	VALUES(nextval('sub_serial'), 1,3,CURRENT_DATE);
	UPDATE STUDENT_CURRENT_WORKSHEET SET w_id = 1 WHERE s_id =1;
COMMIT;

INSERT INTO VOLUNTEER_GRADING_WORKSHEET(sub_id, v_id, w_id, s_id, date)
VALUES(1,1,2,1,CURRENT_DATE);

INSERT INTO VOLUNTEER_GRADING_WORKSHEET(sub_id, v_id,w_id,s_id,date)
VALUES(1,1,2,1,CURRENT_DATE);

BEGIN;
	INSERT INTO GRADED_WORKSHEET(grds_id, s_id, w_id, v_id, language, grade, review)
	VALUES(nextval('grds_serial'),1,2,1, 'Englsih', 90,'good job!');
	DELETE FROM VOLUNTEER_GRADING_WORKSHEET WHERE v_id = (SELECT v_id FROM GRADED_WORKSHEET WHERE grds_id = (SELECT last_value FROM grds_serial));
COMMIT;

SELECT * FROM student_current_worksheet;
SELECT * FROM student_submitted_worksheet;
SELECT * FROM volunteer_grading_worksheet;
SELECT * FROM graded_worksheet;

        """
       # close the communication with the PostgreSQL
        curr.execute(init_sql_lines)
        conn.commit()
        cur.close()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
if __name__ == '__main__':
    connect()

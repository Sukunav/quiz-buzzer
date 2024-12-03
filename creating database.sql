CREATE DATABASE quiz;
USE quiz;
CREATE TABLE quiz_entries (Sno int(2),team varchar(10),pressed varchar(7),reset_entry varchar(5),PRIMARY KEY (Sno));
CREATE TABLE agni(quesno int(2),score int,FOREIGN KEY (quesno) REFERENCES quiz_entries(Sno));
CREATE TABLE neer(quesno int(2),score int,FOREIGN KEY (quesno) REFERENCES quiz_entries(Sno));
CREATE TABLE prithvi(quesno int(2),score int,FOREIGN KEY (quesno) REFERENCES quiz_entries(Sno));
CREATE TABLE vayu(quesno int(2),score int,FOREIGN KEY (quesno) REFERENCES quiz_entries(Sno));

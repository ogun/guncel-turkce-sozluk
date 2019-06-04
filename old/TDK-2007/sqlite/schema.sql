-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

-- That file uses encoding UTF-8

CREATE TABLE `SENSES`
 (
	`WORD_ID`			varchar, 
	`MULT_NO`			varchar, 
	`SENSE_NO`			INTEGER, 
	`VERB`			varchar, 
	`WORD_TYPE1`			varchar, 
	`WORD_TYPE2`			varchar, 
	`WORD_TYPE3`			varchar, 
	`USAGE_TYPE1`			varchar, 
	`USAGE_TYPE2`			varchar, 
	`CONTEXT1`			varchar, 
	`CONTEXT2`			varchar, 
	`MEANING`			TEXT, 
	`CÜMLE`			TEXT
);

CREATE TABLE `WORDMULT`
 (
	`WORD_ID`			varchar, 
	`MULT_NO`			varchar, 
	`PRE_MULT`			varchar, 
	`HEAD_MULT`			varchar, 
	`SUFFIX`			varchar, 
	`PLURAL`			varchar, 
	`SPECIAL`			varchar, 
	`LANGUAGE1`			varchar, 
	`SEE_PRE`			TEXT
);


-- CREATE Relationships ...

import MySQLdb as mdb
from . import credentials as c # Private info loging in to mysql db. not in git repo

def is_already_initialized(cur):
    table_descriptions = (
        ("DESCRIBE istoriai.words", (
            ('id', 'int(10) unsigned', 'NO', 'UNI', None, 'auto_increment'), 
            ('word', 'varchar(45)', 'NO', 'PRI', None, ''))
        ),
        ("DESCRIBE istoriai.submissions", (
			('id', 'char(10)', 'NO', 'PRI', None, ''), 
            ('subredditId', 'char(10)', 'NO', 'PRI', None, ''), 
            ('created_utc', 'int(10) unsigned', 'YES', '', None, ''), 
            ('flesch', 'decimal(5,2)', 'YES', '', None, ''), 
            ('smog', 'decimal(5,2)', 'YES', '', None, ''), 
            ('kincaid', 'decimal(5,2)', 'YES', '', None, ''), 
            ('coleman', 'decimal(5,2)', 'YES', '', None, ''), 
            ('automated', 'decimal(5,2)', 'YES', '', None, ''), 
            ('dale', 'decimal(5,2)', 'YES', '', None, ''), 
            ('diffwords', 'int(10) unsigned', 'YES', '', None, ''), 
            ('linsear', 'decimal(5,2)', 'YES', '', None, ''), 
            ('gunning', 'decimal(5,2)', 'YES', '', None, ''), 
            ('standard', 'decimal(5,2)', 'YES', '', None, ''))
        ),
        ("DESCRIBE istoriai.vocabularies", (
            ('subredditId', 'char(10)', 'NO', 'PRI', None, ''), 
            ('wordId', 'int(10) unsigned', 'NO', 'PRI', None, ''), 
            ('count', 'int(10) unsigned', 'YES', '', None, '')
            )
        ))
    is_initialized = True
    for describe_command_and_result in table_descriptions:
        cur.execute(describe_command_and_result[0])
        is_initialized &= cur.fetchall() == describe_command_and_result[1]
    return is_initialized

def initialize(): 
    con =  mdb.connect(c.get_host(), c.get_user(), c.get_password(), c.get_db())
    with con:
        cur = con.cursor()
        if is_already_initialized(cur):
            return
        
        initialization_script = [
            """ SET NAMES utf8mb4""",
            """ SET CHARACTER SET utf8mb4""", 
            """ SET character_set_connection=utf8mb4""", 
            """ CREATE TABLE IF NOT EXISTS submissions(
                    id CHAR(10),
                    subredditId  CHAR(10), 
                    PRIMARY KEY (
                        id, 
                        subredditId), 
                    created_utc INT UNSIGNED, 
                    flesch DECIMAL(5,2), 
                    smog DECIMAL(5,2), 
                    kincaid DECIMAL(5,2), 
                    coleman DECIMAL(5,2), 
                    automated DECIMAL(5,2), 
                    dale DECIMAL(5,2), 
                    diffwords INTEGER UNSIGNED, 
                    linsear DECIMAL(5,2), 
                    gunning DECIMAL(5,2), 
                    standard DECIMAL(5,2))""", 
            """ CREATE TABLE IF NOT EXISTS words(
                    id INT UNSIGNED AUTO_INCREMENT UNIQUE KEY, 
                    word VARCHAR(45) PRIMARY KEY)""",
            """ CREATE TABLE IF NOT EXISTS vocabularies( 
                    subredditId CHAR(10), 
                    wordId INT UNSIGNED, 
                    count INT UNSIGNED, 
                    PRIMARY KEY (
                        subredditId, 
                        wordId)) """
        ]

        con.set_character_set('utf8mb4')
        for command in initialization_script:
            cur.execute(command)	

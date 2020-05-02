/***********************************************************
*
* MPD Designer 3.1.4150.32424
*
* Code for PostgreSQL 7.4
* Generated on 02/04/2020 16:51:04
*
* Louis SAUNDERS
* http://louis.saunders.free.fr/
*
************************************************************/

--ALTER TABLE environment
--    DROP FOREIGN KEY FK_ENV_APP;


DROP TABLE IF EXISTS environment;
DROP TABLE IF EXISTS configuration;
DROP TABLE IF EXISTS application;


/***********************************************************
* configuration
************************************************************/

CREATE TABLE configuration (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    key TEXT NOT NULL, 
    value TEXT,
    UNIQUE (key)
);

/***********************************************************
* environment
************************************************************/
/*
CREATE TABLE environment (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
    name TEXT NOT NULL, 
    UNIQUE (name)
);
*/

/***********************************************************
* application
************************************************************/

CREATE TABLE application (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    environment TEXT,
    version TEXT,
    country TEXT,
    provider TEXT,
    project TEXT,
    region TEXT,
    datacenter TEXT,
    services TEXT,
    UNIQUE (name, environment)
);


/***********************************************************
* INDEXED KEYS
************************************************************/


/***********************************************************
* FOREIGN KEYS
************************************************************/


/***********************************************************
* DATA
************************************************************/
INSERT INTO configuration (id, key, value) VALUES (1, 'customer', 'Germain');
INSERT INTO application (id, name, environment, provider, project, region) VALUES (1, 'Dartagnan', 'Production', 'AWS', 'Prod', 'Paris');
INSERT INTO application (id, name, environment, provider, country) VALUES (2, 'Dartagnan', 'Preprod', 'AWS', 'France');
INSERT INTO application (id, name, environment, provider, country) VALUES (3, 'Search&Co', 'Production', 'GCP', 'Belgium');
INSERT INTO application (id, name, environment, provider, country) VALUES (4, 'Search&Co', 'Preprod', 'GCP', 'Netherlands');

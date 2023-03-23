CREATE DATABASE IF NOT EXISTS plantsdb;

USE plantsdb;
DROP TABLE IF EXISTS plants;

CREATE TABLE plants (
    Botanical_Name varchar(512),
    Common_Name varchar(512),
    Lowering varchar(512),
    Light varchar(512),
    Temperature varchar(512),
    Humidity varchar(512),
    Watering varchar(512),
    Soil_Mix varchar(2048)
);

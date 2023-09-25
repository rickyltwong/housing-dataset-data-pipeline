DROP TABLE IF EXISTS suburb;
DROP TABLE IF EXISTS type;
DROP TABLE IF EXISTS method;
DROP TABLE IF EXISTS seller;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS councilarea;
DROP TABLE IF EXISTS property;

-- Suburb Table
CREATE TABLE Suburb
(
    suburb_id      SERIAL PRIMARY KEY,
    name           VARCHAR(50) NOT NULL,
    postcode       INTEGER,
    property_count INTEGER     NOT NULL
);

-- Type Table
CREATE TABLE Type
(
    type_code   VARCHAR(10) PRIMARY KEY,
    description VARCHAR(50) NOT NULL
);


-- Method Table
CREATE TABLE Method
(
    method_code VARCHAR(10) PRIMARY KEY,
    description VARCHAR(50) NOT NULL
);

-- Seller Table
CREATE TABLE Seller
(
    seller_id SERIAL PRIMARY KEY,
    name      VARCHAR(50) NOT NULL
);

-- Region Table
CREATE TABLE Region
(
    region_id SERIAL PRIMARY KEY,
    name      VARCHAR(50) NOT NULL
);

-- CouncilArea Table
CREATE TABLE CouncilArea
(
    council_area_id SERIAL PRIMARY KEY,
    name            VARCHAR(50) NOT NULL
);

-- Property Table
CREATE TABLE Property
(
    property_id     SERIAL PRIMARY KEY,
    address         VARCHAR(50),
    rooms           FLOAT,
    bedroom_2       FLOAT,
    bathroom        FLOAT,
    car             FLOAT,
    land_size       FLOAT,
    building_area   FLOAT,
    year_built      FLOAT,
    distance        FLOAT,
    price           FLOAT,
    latitude        FLOAT,
    longitude       FLOAT,
    suburb_id       INTEGER REFERENCES Suburb (suburb_id),
    type_code       VARCHAR(10) REFERENCES Type (type_code),
    seller_id       INTEGER REFERENCES Seller (seller_id),
    method_code     VARCHAR(10) REFERENCES Method (method_code),
    region_id       INTEGER REFERENCES Region (region_id),
    council_area_id FLOAT REFERENCES CouncilArea (council_area_id),
    post_date       DATE
);



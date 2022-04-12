CREATE TABLE alcohol
(
    alcohol_id          serial PRIMARY KEY,
    name                VARCHAR(50) NOT NULL,
    kind                VARCHAR(50) NOT NULL,
    rating              FLOAT,
    type                VARCHAR(50),
    description         VARCHAR(1500),
    region_id           INTEGER,
    alcohol_by_volume   FLOAT,
    color               VARCHAR(50),
    year                INTEGER,
    bitterness_IBU      INTEGER,
    SRM                 FLOAT,
    extract             FLOAT,
    serving_temperature VARCHAR(7),
    brand               VARCHAR(50),
    vine_stock          VARCHAR(50),
    image               BYTEA

);

CREATE TABLE bar_code
(
    bar_code   VARCHAR(13) PRIMARY KEY,
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id)
);


CREATE TABLE country
(
    country_id SERIAL PRIMARY KEY,
    country    VARCHAR(50)
);

CREATE TABLE region
(
    region_id  serial PRIMARY KEY,
    region_name VARCHAR(50),
    country_id INTEGER REFERENCES country (country_id)
);

CREATE TABLE food
(
    food_id   SERIAL PRIMARY KEY,
    food_name VARCHAR(50)
);

CREATE TABLE aroma
(
    aroma_id   SERIAL PRIMARY KEY,
    aroma_name VARCHAR(50)
);
CREATE TABLE flavour
(
    flavour_id   SERIAL PRIMARY KEY,
    flavour_name VARCHAR(50)
);
CREATE TABLE ingredient
(
    ingredient_id   SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(50)
);


CREATE TABLE alcohol_aroma
(
    flavour_id INTEGER REFERENCES aroma (aroma_id),
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id)
);

CREATE TABLE alcohol_food_pairing
(
    food_id    INTEGER REFERENCES food (food_id),
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id)
);

CREATE TABLE alcohol_flavour
(
    flavour_id INTEGER REFERENCES flavour (flavour_id),
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id)
);
CREATE TABLE alcohol_ingredient
(
    flavour_id INTEGER REFERENCES ingredient (ingredient_id),
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id)
);

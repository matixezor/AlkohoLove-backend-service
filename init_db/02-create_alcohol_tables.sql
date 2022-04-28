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
    age                 Integer,
    bitterness_ibu      INTEGER,
    srm                 FLOAT,
    extract             FLOAT,
    fermentation        VARCHAR(11),
    is_filtered         BOOLEAN,
    is_pasteurized      BOOLEAN,
    serving_temperature VARCHAR(7),
    manufacturer        VARCHAR(50),
    vine_stock          VARCHAR(50),
    image_name          VARCHAR(50)
);

CREATE TABLE barcode
(
    barcode    VARCHAR(13) PRIMARY KEY,
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE
);

CREATE TABLE country
(
    country_id      SERIAL PRIMARY KEY,
    country_name    VARCHAR(50)
);

CREATE INDEX ON country (country_name);

CREATE TABLE region
(
    region_id   serial PRIMARY KEY,
    region_name VARCHAR(50),
    country_id  INTEGER REFERENCES country (country_id) ON DELETE CASCADE
);

CREATE INDEX ON region (region_name);

CREATE TABLE food
(
    food_id   SERIAL PRIMARY KEY,
    food_name VARCHAR(50)
);

CREATE TABLE ingredient
(
    ingredient_id   SERIAL PRIMARY KEY,
    ingredient_name VARCHAR(50)
);

CREATE TABLE flavour
(
    flavour_id   SERIAL PRIMARY KEY,
    flavour_name VARCHAR(50)
);

CREATE TABLE alcohol_food
(
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    food_id    INTEGER REFERENCES food (food_id) ON DELETE CASCADE,
    PRIMARY KEY (food_id, alcohol_id)

);

CREATE TABLE alcohol_aroma
(
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    flavour_id INTEGER REFERENCES flavour (flavour_id) ON DELETE CASCADE,
    PRIMARY KEY (flavour_id, alcohol_id)
);


CREATE TABLE alcohol_taste
(
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    flavour_id INTEGER REFERENCES flavour (flavour_id) ON DELETE CASCADE,
    PRIMARY KEY (flavour_id, alcohol_id)
);

CREATE TABLE alcohol_finish
(
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    flavour_id INTEGER REFERENCES flavour (flavour_id) ON DELETE CASCADE,
    PRIMARY KEY (flavour_id, alcohol_id)
);

CREATE TABLE alcohol_ingredient
(
    alcohol_id    INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    ingredient_id INTEGER REFERENCES ingredient (ingredient_id) ON DELETE CASCADE,
    PRIMARY KEY (ingredient_id, alcohol_id)
);

CREATE INDEX ON flavour (flavour_name);
CREATE INDEX ON ingredient (ingredient_name);
CREATE TABLE alcohol
(
    alcohol_id          serial PRIMARY KEY,
    name                VARCHAR(50),
    type                VARCHAR(50),
    description         VARCHAR(1500),
    alcohol_by_volume   FLOAT,
    rating              FLOAT,
    country             VARCHAR(50),
    region              VARCHAR(50),
    color               VARCHAR(50),
    vintage             INTEGER,
    bitterness_IBU      INTEGER,
    style               VARCHAR(50),
    SRM                 float,
    BLG                 FLOAT,
    serving_temperature VARCHAR(7),
    extract             FLOAT,
    brand               VARCHAR(50),
    kind                VARCHAR(50),
    image               VARCHAR(50),
    ingredient          VARCHAR(50)
);

CREATE TABLE bar_code
(
    bar_code   CHAR(13) PRIMARY KEY,
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id)
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

CREATE TABLE reported_error
(
 error_id    serial PRIMARY KEY,
 user_id     INTEGER REFERENCES users (user_id),
 description VARCHAR(500) NOT NULL
);

CREATE TABLE alcohol_request
(
    request_id          serial PRIMARY KEY,
    user_id             INTEGER REFERENCES users (user_id),
    name                VARCHAR(50) NOT NULL,
    kind                VARCHAR(50) NOT NULL,
    type                VARCHAR(50) NOT NULL,
    alcohol_by_volume   FLOAT,
    color               VARCHAR(50),
    year                INTEGER,
    bitterness_IBU      INTEGER,
    SRM                 FLOAT,
    extract             FLOAT,
    fermentation        VARCHAR(11),
    is_filtered         BOOLEAN,
    is_pasteurized      BOOLEAN,
    brand               VARCHAR(50) NOT NULL,
    vine_stock          VARCHAR(50),
    barcode             VARCHAR(50) NOT NULL,
    country             VARCHAR(50),
    region              VARCHAR(50),
    image               BYTEA NOT NULL
);
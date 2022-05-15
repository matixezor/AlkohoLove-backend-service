CREATE TABLE user_favourite_alcohol
(
    user_id    INTEGER REFERENCES Users (user_id) ON DELETE CASCADE,
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, alcohol_id)
);

CREATE TABLE user_wishlist
(
    user_id    INTEGER REFERENCES Users (user_id) ON DELETE CASCADE,
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, alcohol_id)
);

CREATE TABLE user_search_history
(
    user_id    INTEGER REFERENCES Users (user_id) ON DELETE CASCADE,
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    date       TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, alcohol_id, date)
);
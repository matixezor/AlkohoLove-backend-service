CREATE TABLE user_tag
(
    tag_id          serial PRIMARY KEY,
    tag_name        VARCHAR(50) NOT NULL,
    user_id         INTEGER REFERENCES Users (user_id) ON DELETE CASCADE NOT NULL
);

CREATE TABLE alcohol_user_tag
(
    alcohol_id INTEGER REFERENCES alcohol (alcohol_id) ON DELETE CASCADE,
    tag_id   INTEGER REFERENCES user_tag (tag_id) ON DELETE CASCADE,
    PRIMARY KEY (tag_id, alcohol_id)
);
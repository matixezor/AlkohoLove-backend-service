CREATE TABLE token_blacklist (
	token_jti VARCHAR( 36 ) PRIMARY KEY,
	expiration_date TIMESTAMP NOT NULL
);

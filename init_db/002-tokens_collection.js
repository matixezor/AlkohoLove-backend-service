let token = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['token_jti', 'expiration_date'],
        properties: {
            token_jti: {
                bsonType: 'string',
                description: 'must be a string'
            },
            expiration_date: {
                bsonType: 'date',
                description: 'must be a date'
            }
        }
    }
}

db.createCollection(
    'tokens_blacklist',
    {
        validator: token,
    }
)

db.tokens_blacklist.createIndex({token_jti: 1})
db.tokens_blacklist.createIndex({expiration_date: 1}, {expireAfterSeconds: 10})

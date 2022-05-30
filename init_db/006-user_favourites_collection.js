let favourite = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['user_id', 'alcohols'],
        properties: {
            user_id: {
                bsonType: 'objectId',
                description: 'must be an objectId'
            },
            alcohols: {
                bsonType: 'array',
                description: 'list of alcohols',
                items: {
                    bsonType: 'objectId'
                }
            }
        }
    }
}


db.createCollection(
    'user_favourites',
    {
        validator: favourite
    }
)

db.user_favourites.createIndex({user_id: 1})

db.user_favourites.insertMany(
    [
        {
            _id: ObjectId('6291334d308b89e057643c6d'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            alcohols: [ ObjectId('6288e32dd5ab6070dde8db8b')]
        },
        {
            _id: ObjectId('62913353613d3b9a79f89008'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            alcohols: [ ObjectId('6288e32dd5ab6070dde8db8c'),  ObjectId('6288e32dd5ab6070dde8db8e')]
        },
        {
            _id: ObjectId('62913358cce583b10e5a8d31'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            alcohols: [ ObjectId('6288e32dd5ab6070dde8db8a'),  ObjectId('6288e32dd5ab6070dde8db8c'),  ObjectId('6288e32dd5ab6070dde8db8e'),  ObjectId('6288e32dd5ab6070dde8db8f')]
        }
    ]
)

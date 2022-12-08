let wishlist = {
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
    'user_wishlist',
    {
        validator: wishlist
    }
)

db.user_wishlist.createIndex({user_id: 1})

db.user_wishlist.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            alcohols: [ ObjectId('6288e32dd5ab6070dde8db8a')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            alcohols: [ ObjectId('6288e32dd5ab6070dde8db8a'),  ObjectId('6288e32dd5ab6070dde8db8b')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            alcohols: [ ObjectId('6288e32dd5ab6070dde8db8a'),  ObjectId('6288e32dd5ab6070dde8db8b'),  ObjectId('6288e32dd5ab6070dde8db8c'),  ObjectId('6288e32dd5ab6070dde8db8e'),  ObjectId('6288e32dd5ab6070dde8db8f')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            alcohols: []
        }
    ]
)

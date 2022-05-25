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
                    bsonType: 'string'
                }
            },
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
            alcohols: ['6288e32dd5ab6070dde8db8a']
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            alcohols: ['6288e32dd5ab6070dde8db8a', '6288e32dd5ab6070dde8db8b']
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            alcohols: ['6288e32dd5ab6070dde8db8c', '6288e32dd5ab6070dde8db8e', '6288e32dd5ab6070dde8db8f', '6288e32dd5ab6070dde8db8c', '6288e32dd5ab6070dde8db8b', '6288e32dd5ab6070dde8db8a']
        }
    ]
)

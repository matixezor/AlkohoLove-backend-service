let following = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['following_users'],
        properties: {
            following_users: {
                bsonType: 'array',
                description: 'list of users following given user',
                items: {
                    bsonType: 'objectId'
                }
            }
        }
    }
}


db.createCollection(
    'following_users',
    {
        validator: following
    }
)


db.following_users.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            following_users: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8d')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            following_users: [ObjectId('6288e2fdd5ab6070dde8db8d'), ObjectId('6288e2fdd5ab6070dde8db8b')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            following_users: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8b')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            following_users: []
        }
    ]
)

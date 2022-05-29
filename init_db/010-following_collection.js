let following_entry = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['following'],
        properties: {
            following: {
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
    'following',
    {
        validator: following_entry
    }
)


db.following.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            following: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8d')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            following: [ObjectId('6288e2fdd5ab6070dde8db8d'), ObjectId('6288e2fdd5ab6070dde8db8b')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            following: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8b')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            following: []
        }
    ]
)

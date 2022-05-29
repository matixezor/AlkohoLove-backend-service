let followed = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['followed_by'],
        properties: {
            followed_users: {
                bsonType: 'array',
                description: 'list of users followed by given user',
                items: {
                    bsonType: 'objectId'
                }
            }
        }
    }
}


db.createCollection(
    'followed_by',
    {
        validator: followed
    }
)


db.followed_by.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            followed_by: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8d')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            followed_by: [ObjectId('6288e2fdd5ab6070dde8db8b'), ObjectId('6288e2fdd5ab6070dde8db8d')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            followed_by: [ObjectId('6288e2fdd5ab6070dde8db8b'), ObjectId('6288e2fdd5ab6070dde8db8c')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            followed_by: []
        }
    ]
)

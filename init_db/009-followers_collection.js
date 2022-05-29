let followed_entry = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['followers'],
        properties: {
            followers: {
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
    'followers',
    {
        validator: followed_entry
    }
)


db.followers.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            followers: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8d')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            followers: [ObjectId('6288e2fdd5ab6070dde8db8b'), ObjectId('6288e2fdd5ab6070dde8db8d')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            followers: [ObjectId('6288e2fdd5ab6070dde8db8b'), ObjectId('6288e2fdd5ab6070dde8db8c')]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            followers: []
        }
    ]
)

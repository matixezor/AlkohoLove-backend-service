let error = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['user_id', 'description'],
        properties: {
            user_id: {
                bsonType: 'objectId',
                description: 'must be an objectId'
            },
            description: {
                bsonType: 'string',
                description: 'must be a string'
            }
        }
    }
}

db.createCollection(
    'reported_errors',
    {
        validator: error
    }
)

db.reported_errors.createIndex({user_id: 1})

db.reported_errors.insertMany(
    [
        {
            _id: ObjectId('507f191e810c19729de860ea'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            description: 'This app sucks'
        },
        {
            _id: ObjectId('507f191e810c19729de860eb'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            description: 'This app sucks very much'
        },
        {
            _id: ObjectId('507f191e810c19729de860ec'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            description: 'Pagination does not work'
        }
    ]
)

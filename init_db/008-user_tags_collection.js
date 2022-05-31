let tag = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['user_id', 'tag_name', 'alcohols'],
        properties: {
            user_id: {
                bsonType: 'objectId',
                description: 'must be an objectId'
            },
            tag_name: {
                bsonType: 'string',
                description: 'must be a string'
            },
            alcohols: {
                bsonType: 'array',
                description: 'list of alcohol ids',
                items: {
                    bsonType: 'objectId'
                }
            }
        }
    }
}


db.createCollection(
    'user_tags',
    {
        validator: tag
    }
)

db.user_tags.createIndex({user_id: 1})

db.user_tags.insertMany(
    [
        {
            _id: ObjectId('628f9071f32df3b39ced1a3a'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            tag_name: 'grill u huberta',
            alcohols: [ObjectId('6288e32dd5ab6070dde8db8a')]
        },
        {
            _id: ObjectId('628f9071f32df3b39ced1a3b'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            tag_name: 'wakacje 2021',
            alcohols: [ObjectId('6288e32dd5ab6070dde8db8a'), ObjectId('6288e32dd5ab6070dde8db8c')]
        },
        {
            _id: ObjectId('628f9071f32df3b39ced1a3c'),
            user_id: ObjectId('507f191e810c19729de860eb'),
            tag_name: 'wakacje 2022',
            alcohols: [ObjectId('6288e32dd5ab6070dde8db8e'), ObjectId('6288e32dd5ab6070dde8db8f'), ObjectId('6288e32dd5ab6070dde8db8c'), ObjectId('6288e32dd5ab6070dde8db8b'), ObjectId('6288e32dd5ab6070dde8db8a')]
        }
    ]
)
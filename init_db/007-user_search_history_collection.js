let search = {
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
                description: 'list of alcohols with dates',
                items: {
                    properties: {
                        alcohol_id: {
                            bsonType: 'objectId',
                            description: 'must be an objectId'
                        },
                        search_date: {
                            bsonType: 'date',
                            description: 'must be a date'
                        }
                    }
                }
            }
        }
    }
}


db.createCollection(
    'user_search_history',
    {
        validator: search
    }
)

db.user_search_history.createIndex({user_id: 1})

db.user_search_history.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            alcohols: [
                {
                    alcohol_id: ObjectId('6288e32dd5ab6070dde8db8a'),
                    search_date: new ISODate('2022-03-21T19:13:25Z')
                }
            ]
        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            alcohols: [
                {
                    alcohol_id: ObjectId('6288e32dd5ab6070dde8db8a'),
                    search_date: new ISODate('2022-04-25T19:13:25Z')
                },
                {
                    alcohol_id: ObjectId('6288e32dd5ab6070dde8db8b'),
                    search_date: new ISODate('2022-07-21T19:13:25Z')
                }]
        }
    ]
)

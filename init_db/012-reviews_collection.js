let alcohol_review = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['user_id', 'username','alcohol_id','review','rating','date','report_count','reporters'],
        properties: {
            user_id: {
                bsonType: 'objectId',
                description: 'must be an objectId'
            },
            username: {
                bsonType: 'string',
                description: 'must be a string'
            },
            alcohol_id: {
                bsonType: 'objectId',
                description: 'must be an objectId'
            },
            review: {
                bsonType: ['string', 'null'],
                description: 'must be a string'
            },
            rating: {
                bsonType: 'int',
                description: 'must be an integer'
            },
             date: {
                bsonType: 'date',
                description: 'must be a date'
            },
            report_count: {
                bsonType: 'int',
                description: 'must be an integer'
            },
            reporters: {
                bsonType: 'array',
                description: 'list of user ids',
                items: {
                    bsonType: 'objectId'
                }
            },
            helpful_count: {
                bsonType: 'int',
                description: 'must be an integer'
            },
        }
    }
}

db.createCollection(
    'reviews',
    {
        validator: alcohol_review
    }
)

db.reviews.createIndex({alcohol_id: 1})

db.reviews.insertMany(
    [
        {
            _id: ObjectId('62964f8f12ce37ef94d3cbaa'),
            username: 'Adam_Skorupa',
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            alcohol_id: ObjectId('6288e32dd5ab6070dde8db8a'),
            review: 'Pyszniutkie polecam',
            rating: NumberInt(5),
            date: new ISODate('2022-04-14T11:11:23Z'),
            report_count: NumberInt(0),
            reporters: [],
            helpful_count: NumberInt(0),
            helpful_reporters: [],
        },
        {
            _id: ObjectId('62964f8f12ce37ef94d3cbab'),
            username: 'Adam_Skorupa',
            user_id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            alcohol_id: ObjectId('6288e32dd5ab6070dde8db8b'),
            review: 'ok',
            rating: NumberInt(5),
            date: new ISODate('2022-05-13T15:22:32Z'),
            report_count: NumberInt(0),
            reporters: [],
            helpful_count: NumberInt(0),
            helpful_reporters: [],
        },
        {
            _id: ObjectId('6296768d872c15947e569b97'),
            username: 'DariuszGołąbski',
            user_id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            alcohol_id: ObjectId('6288e32dd5ab6070dde8db8b'),
            review: 'DO DU**Y',
            rating: NumberInt(1),
            date: new ISODate('2022-05-15T12:42:32Z'),
            report_count: NumberInt(1),
            reporters: [ObjectId('6288e2fdd5ab6070dde8db8b')],
            helpful_count: NumberInt(1),
            helpful_reporters: [ObjectId('6288e2fdd5ab6070dde8db8c')],
        }
    ]
)
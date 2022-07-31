let alcohol_review = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['user_id', 'username','alcohol_id','review','rating','date','report_count','reporters','reason','ban_date'],
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
            ban_date: {
                bsonType: 'date',
                description: 'must be a date'
            },
            reason: {
                bsonType: ['string', 'null'],
                description: 'must be a string'
            }
        }
    }
}

db.createCollection(
    'banned_reviews',
    {
        validator: alcohol_review
    }
)

db.banned_reviews.createIndex({user_id: 1})

db.banned_reviews.insertMany(
    [
        {
            _id: ObjectId('6296768d872c15947e569b96'),
            username: 'DariuszGołąbski',
            user_id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            alcohol_id: ObjectId('6288e32dd5ab6070dde8db8c'),
            review: 'DO DU**Y!!!',
            rating: NumberInt(1),
            date: new ISODate('2022-05-15T12:43:32Z'),
            report_count: NumberInt(2),
            reporters: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8b')],
            ban_date: new ISODate('2022-07-31T13:54:29.671972'),
            reason: 'Wulgaryzm!'
        }
    ]
)
let suggestion = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['user_id', 'barcode', 'kind', 'name'],
        properties: {
            user_id: {
                bsonType: 'array',
                description: 'must be an objectId',
                items: {
                    bsonType: 'objectId'
                }
            },
            barcode: {
                title: 'kod kreskowy',
                bsonType: 'string',
                description: '123456789',
            },
            kind: {
                title: 'kategoria',
                bsonType: 'string',
                description: 'whisky'
            },
            name: {
                title: 'nazwa',
                bsonType: 'string',
                description: 'Jameson'
            },
            description: {
                title: 'opis',
                bsonType: 'array',
                description: 'Pyszna whisky',
                items: {
                    bsonType: 'string'
                }
            }
        }
    }
}


db.createCollection(
    'alcohol_suggestion',
    {
        validator: suggestion
    }
)


db.alcohol_suggestion.insertMany(
    [
        {
            _id: ObjectId('6299e8c94105e843197376fd'),
            user_id: [ObjectId('6288e2fdd5ab6070dde8db8c')],
            barcode: '5900699104827',
            kind: 'piwo',
            name: 'Żywiec białe',
            description: ['Białe piwo pszeniczne żywiec.', 'Dobre piwo o aromacie kolendry.']
        },
        {
            _id: ObjectId('6299eb5a894d907992ecbd7e'),
            user_id: [ObjectId('6288e2fdd5ab6070dde8db8d')],
            barcode: '3800006901502',
            kind: 'wino',
            name: 'Witosha premium sweet red',
            description: ['Czerwone wino deserowe słodkie.']
        },
        {
            _id: ObjectId('6299eb5f31a05c42142ea55c'),
            user_id: [ObjectId('6288e2fdd5ab6070dde8db8c'), ObjectId('6288e2fdd5ab6070dde8db8d')],
            barcode: '1111111111111',
            kind: 'likier',
            name: 'Jagermaister',
            description: ['Dobry likier ziołowy.']
        }
    ]
)

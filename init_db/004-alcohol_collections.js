let core = {
    title: 'core',
    required: [
        'barcode',
        'kind',
        'name',
        'type',
        'description',
        'alcohol_by_volume',
        'color',
        'country',
        'region',
        'manufacturer',
        'food',
        'taste',
        'aroma',
        'finish',
        'rate_count',
        'rate_value',
        'avg_rating',
        'keywords'
    ],
    properties: {
        barcode: {
            title: 'kod kreskowy',
            bsonType: 'array',
            description: '123456789',
            items: {
                bsonType: 'string'
            }
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
        type: {
            title: 'typ',
            bsonType: 'string',
            description: 'blended'
        },
        description: {
            title: 'opis',
            bsonType: 'string',
            description: 'Pyszna whisky'
        },
        alcohol_by_volume: {
            title: 'zawartość alkoholu',
            bsonType: 'double',
            description: '40'
        },
        color: {
            title: 'kolor',
            bsonType: 'string',
            description: 'karmelowy'
        },
        country: {
            title: 'kraj',
            bsonType: 'string',
            description: 'Irlandia'
        },
        region: {
            title: 'region',
            bsonType: ['string', 'null'],
            description: 'Cork'
        },
        manufacturer: {
            title: 'producent',
            bsonType: 'string',
            description: 'Irish Distillers'
        },
        food: {
            title: 'jedzenie',
            bsonType: 'array',
            description: 'orzeszki',
            items: {
                bsonType: 'string'
            }
        },
        taste: {
            title: 'smak',
            bsonType: 'array',
            description: 'wanilia',
            items: {
                bsonType: 'string'
            }
        },
        aroma: {
            title: 'aromat',
            bsonType: 'array',
            description: 'nuty korzenne',
            items: {
                bsonType: 'string'
            }
        },
        finish: {
            title: 'finisz',
            bsonType: 'array',
            description: 'łagodny',
            items: {
                bsonType: 'string'
            }
        },
        rate_count: {
            title: 'liczba ocen',
            bsonType: 'long',
            description: '10'
        },
        rate_value: {
            title: 'suma ocen',
            bsonType: 'long',
            description: '50'
        },
        avg_rating: {
            title: 'średnia ocen',
            bsonType: 'double',
            description: '5.0'
        },
        keywords: {
            title: 'tagi',
            bsonType: 'array',
            description: 'irlandzka',
            items: {
                bsonType: 'string'
            }
        }
    }
}

let beer = {
    title: 'piwo',
    required: [
        'ibu',
        'srm',
        'extract',
        'fermentation',
        'is_filtered',
        'is_pasteurized'
    ],
    properties: {
        kind: {
            enum: ['piwo']
        },
        ibu: {
            title: 'ibu',
            bsonType: ['int', 'null'],
            description: '4'
        },
        srm: {
            title: 'srm',
            bsonType: ['double', 'null'],
            description: '4'
        },
        extract: {
            title: 'ekstrakt',
            bsonType: ['double', 'null'],
            description: '11.6'
        },
        fermentation: {
            title: 'fermentacja',
            bsonType: ['string'],
            description: 'górna'
        },
        is_filtered: {
            title: 'filtrowane',
            bsonType: ['bool'],
            description: 'true'
        },
        is_pasteurized: {
            title: 'pasteryzowane',
            bsonType: ['bool'],
            description: 'true'
        },
    }
}

let whisky = {
    title: 'whisky',
    required: ['age'],
    properties: {
        kind: {
            enum: ['whisky']
        },
        age: {
            title: 'wiek',
            bsonType: 'int',
            description: '3'
        }
    }
}

let vodka = {
    title: 'wódka',
    properties: {
        kind: {
            enum: ['wódka']
        }
    }
}

let wine = {
    title: 'wino',
    required: ['vine_strain', 'winery'],
    properties: {
        kind: {
            enum: ['wino']
        },
        vine_strain: {
            title: 'szczep',
            bsonType: ['string', 'null'],
            description: 'Chardonnay'
        },
        winery: {
            title: 'winiarnia',
            bsonType: ['string', 'null'],
            description: 'Château de Cremat'
        }
    }
}

let rum = {
    title: 'rum',
    required: ['age'],
    properties: {
        kind: {
            enum: ['rum']
        },
        age: {
            title: 'wiek',
            bsonType: ['int', 'null'],
            description: '3'
        }
    }
}

let liqueur = {
    title: 'likier',
    properties: {
        kind: {
            enum: ['likier']
        }
    }
}

db.createCollection('alcohol_categories')
db.alcohol_categories.createIndex({title: 1})

db.alcohol_categories.insertMany(
    [
        core,
        beer,
        whisky,
        vodka,
        wine,
        rum,
        liqueur
    ]
)

let alcohol = {
    $jsonSchema: {
        bsonType: 'object',
        required: core.required,
        properties: core.properties,
        oneOf: [
            beer,
            whisky,
            vodka,
            wine,
            rum,
            liqueur
        ]
    }
}

db.createCollection(
    'alcohols',
    {
        validator: alcohol,
    }
)

db.alcohols.createIndex(
    {barcode: 1}
)

db.alcohols.createIndex(
    {
        name: 'text',
        kind: 'text',
        type: 'text',
        color: 'text',
        description: 'text',
        keywords: 'text'
    },
    {
        weights: {
            name: 15,
            kind: 8,
            type: 7,
            color: 5,
            keywords: 3,
        },
        name: 'AlcoholsTextIndex'
    }
)

db.alcohols.insertMany(
    [
        {
            _id: ObjectId('6288e32dd5ab6070dde8db8a'),
            barcode: ['5011007003234', '5011007015534', '5011007003005'],
            kind: 'whisky',
            name: 'Jameson',
            type: 'blended',
            description: 'Lorem ipsum',
            alcohol_by_volume: 40.0,
            color: 'bursztyn',
            country: 'Irlandia',
            region: 'Cork',
            manufacturer: 'Irish Distillers',
            food: ['czekoladowy mus'],
            taste: ['nuty korzenne', 'orzechy', 'wanilia', 'słodkie sherry', 'łagodny'],
            aroma: ['kwiaty', 'owoce', 'nuty korzenne', 'drewno'],
            finish: ['gładki', 'słodki', 'pikantny'],
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            avg_rating: 0.0,
            age: NumberInt(4),
            keywords: ['czteroletnia', 'irlandzka', 'irlandzkie', 'blend']
        },
        {
            _id: ObjectId('6288e32dd5ab6070dde8db8b'),
            barcode: ['5011007025427'],
            kind: 'whisky',
            name: 'Jameson Caskmates Stout Edition',
            type: 'blended',
            description: 'Lorem ipsum',
            alcohol_by_volume: 40.0,
            color: 'karmel',
            country: 'Irlandia',
            region: 'Cork',
            manufacturer: 'Irish Distillers',
            food: ['ser'],
            taste: ['mleczna czekolada', 'chmiel', 'kakao', 'marcepan'],
            aroma: ['owoce', 'jabłko', 'gruszka', 'nuty korzenne', 'orzechy', 'skórka limonki'],
            finish: ['długi', 'słodki', 'mleczna czekolada', 'karmel'],
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            avg_rating: 0.0,
            age: NumberInt(4),
            keywords: ['czteroletnia', 'irlandzka', 'irlandzkie', 'blend', 'piwo']
        },
        {
            _id: ObjectId('6288e32dd5ab6070dde8db8c'),
            barcode: ['7312040017072'],
            kind: 'wódka',
            name: 'Absolut Vodka',
            type: 'czysta',
            description: 'Lorem ipsum',
            alcohol_by_volume: 40.0,
            color: 'bezbarwny',
            country: 'Szwecja',
            region: 'Ahus',
            manufacturer: 'The Absolut Company',
            food: [],
            taste: [],
            aroma: [],
            finish: [],
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            avg_rating: 0.0,
            keywords: ['szwedzka']
        },
        {
            _id: ObjectId('6288e32dd5ab6070dde8db8e'),
            barcode: ['5900595008427'],
            kind: 'likier',
            name: 'Kupnik Pigwa',
            type: 'owocowy',
            description: 'Lorem ipsum',
            alcohol_by_volume: 30.0,
            color: 'pomarańczowy',
            country: 'Polska',
            region: null,
            manufacturer: 'Sobieski Sp. z o.o.',
            food: [],
            taste: ['pigwa'],
            aroma: [],
            finish: [],
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            avg_rating: 0.0,
            keywords: ['wódka', 'pigwowa', 'pigwowy']
        },
        {
            _id: ObjectId('6288e32dd5ab6070dde8db8f'),
            barcode: ['8501110080231'],
            kind: 'rum',
            name: 'Havana Cub Anejo 3 Anos Blanco',
            type: 'biały',
            description: 'Lorem ipsum',
            alcohol_by_volume: 37.5,
            color: 'biały',
            country: 'Kuba',
            region: 'Ahus',
            manufacturer: 'Corporación Cuba Ron',
            food: [],
            taste: ['owoce', 'banany', 'gruszki', 'cynamon', 'pieprz'],
            aroma: ['pieprz', 'lukrecja', 'gruszka', 'cytrusy', 'toffi'],
            finish: ['średnio długi', 'lekka goryczka'],
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            avg_rating: 0.0,
            age: NumberInt(3),
            keywords: ['kubański']
        },
    ]
)
db.createUser(
    {
        user: 'alkoholove_admin',
        pwd: 'Test1234',
        roles: [
            {
                role: "readWriteAnyDatabase",
                db: "admin"
            },
            {
                role: "dbAdminAnyDatabase",
                db: "admin"
            },
            {
                role: "clusterAdmin",
                db: "admin"
            }
        ]
    }
);

let users = {
    $jsonSchema: {
        bsonType: 'object',
        required: ['username', 'password', 'email', 'created_on', 'password_salt'],
        properties: {
            username: {
                bsonType: 'string',
                description: 'must be a string and is required'
            },
            password: {
                bsonType: 'string',
                description: 'must be a string and is required'
            },
            email: {
                bsonType: 'string',
                description: 'must be a string and is required'
            },
            created_on: {
                bsonType: 'date',
                description: 'must be a date'
            },
            password_salt: {
                bsonType: 'string',
                description: 'must be a string and is required'
            },
            last_login: {
                bsonType: ['date', 'null'],
                description: 'must be a date'
            },
            is_admin: {
                bsonType: 'bool',
                description: 'must be a boolean'
            },
            is_banned: {
                bsonType: 'bool',
                description: 'must be a boolean'
            },
            rate_count: {
                bsonType: 'long',
                description: '10'
            },
            rate_value: {
                bsonType: 'long',
                description: '50'
            },
            avg_rating: {
                bsonType: 'double',
                description: '5.0'
            },
            following_count: {
                bsonType: 'int',
                description: '5'
            },
            followers_count: {
                bsonType: 'int',
                description: '5'
            },
            favourites_count: {
                bsonType: 'int',
                description: '5'
            },
            is_verified: {
                bsonType: 'bool',
                description: 'must be a bool'
            },
            verification_code: {
                bsonType: ['string', 'null'],
                description: 'must be a str or null'
            },
            reset_password_code: {
                bsonType: ['string', 'null'],
                description: 'must be a str or null'
            },
            delete_account_code: {
                bsonType: ['string', 'null'],
                description: 'must be a str or null'
            },
            updated_at: {
                bsonType: 'date',
                description: 'must be a date'
            },
        }
    }
}

db.createCollection(
    'users',
    {
        validator: users,
    }
)

db.users.createIndex({username: 1})
db.users.createIndex({email: 1})

db.users.insertMany(
    [
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8b'),
            username: 'admin',
            password: '$2b$12$6MDWT6CUgpAnva9fMnL0N.cGGDRyy5xcR472RiHA5pCSQZ.ZUvvk6',
            email: 'admin@gmail.com',
            created_on: new ISODate('2022-03-22T19:10:25Z'),
            last_login: new ISODate('2022-03-22T19:13:25Z'),
            is_admin: true,
            is_banned: false,
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO',
            avg_rating: 0.0,
            favourites_count: NumberInt(1),
            followers_count: NumberInt(2),
            following_count: NumberInt(2),
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            is_verified: true,
            verification_code: null,
            reset_password_code: null,
            delete_account_code: null,
            updated_at: new ISODate('2022-03-22T19:10:25Z')

        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8c'),
            username: 'Adam_Skorupa',
            password: '$2b$12$6MDWT6CUgpAnva9fMnL0N.cGGDRyy5xcR472RiHA5pCSQZ.ZUvvk6',
            email: 'adam.skorupa@gmail.com',
            created_on: new ISODate('2022-04-12T06:11:15Z'),
            last_login: new ISODate('2022-04-22T16:24:21Z'),
            is_admin: false,
            is_banned: false,
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO',
            avg_rating: 5.0,
            favourites_count: NumberInt(2),
            followers_count: NumberInt(2),
            following_count: NumberInt(2),
            rate_count: NumberLong(2),
            rate_value: NumberLong(10),
            is_verified: true,
            verification_code: null,
            reset_password_code: null,
            delete_account_code: null,
            updated_at: new ISODate('2022-03-22T19:10:25Z')

        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8d'),
            username: 'DariuszGołąbski',
            password: '$2b$12$6MDWT6CUgpAnva9fMnL0N.cGGDRyy5xcR472RiHA5pCSQZ.ZUvvk6',
            email: 'dariusz.golabski@gmail.com',
            created_on: new ISODate('2022-01-08T08:16:42Z'),
            last_login: new ISODate('2022-04-21T12:32:43Z'),
            is_admin: false,
            is_banned: false,
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO',
            avg_rating: 1.0,
            favourites_count: NumberInt(4),
            followers_count: NumberInt(2),
            following_count: NumberInt(2),
            rate_count: NumberLong(1),
            rate_value: NumberLong(1),
            is_verified: true,
            verification_code: null,
            reset_password_code: null,
            delete_account_code: null,
            updated_at: new ISODate('2022-03-22T19:10:25Z')

        },
        {
            _id: ObjectId('6288e2fdd5ab6070dde8db8e'),
            username: 'ZbanowanyJeleń',
            password: '$2b$12$6MDWT6CUgpAnva9fMnL0N.cGGDRyy5xcR472RiHA5pCSQZ.ZUvvk6',
            email: 'jeleń@gmail.com',
            created_on: new ISODate('2022-01-08T08:16:42Z'),
            last_login: new ISODate('2022-04-21T12:32:43Z'),
            is_admin: false,
            is_banned: true,
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO',
            avg_rating: 0.0,
            favourites_count: NumberInt(0),
            followers_count: NumberInt(0),
            following_count: NumberInt(1),
            rate_count: NumberLong(0),
            rate_value: NumberLong(0),
            is_verified: true,
            verification_code: null,
            reset_password_code: null,
            delete_account_code: null,
            updated_at: new ISODate('2022-03-22T19:10:25Z')


        }
    ]
)

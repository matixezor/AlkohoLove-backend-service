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
                role : "dbAdminAnyDatabase",
                db : "admin"
            },
            {
                role : "clusterAdmin",
                db : "admin"
            }
        ]
    }
);

let users = {
    $jsonSchema: {
        bsonType: 'object',
        required: [ 'username', 'password', 'email', 'created_on', 'password_salt' ],
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
            }
        }
    }
}

db.createCollection(
    'users',
    {
     validator: users,
    }
)

db.users.createIndex( { username: 1 } )
db.users.createIndex( { email: 1 } )

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
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO'
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
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO'
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
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO'
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
            password_salt: '$2b$12$9z2iZlb2xzIOsZC0ws1pEO'
        },
    ]
)

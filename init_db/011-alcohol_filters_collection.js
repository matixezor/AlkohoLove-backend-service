db.createCollection(
    'alcohol_filters'
)

db.alcohols.aggregate([
    {
        $group: {
            _id: "$kind",
            type: {$addToSet: '$type'},
            color: {$addToSet: '$color'},
            country: {$addToSet: '$country'},
        }
    },
    {
        $merge: {
            into: "alcohol_filters"
        }
    }
])

db.alcohol_filters.insertOne(
    {
        _id: "all",
        type: db.alcohols.distinct('type'),
        color: db.alcohols.distinct('color'),
        country: db.alcohols.distinct('country'),
    }
)
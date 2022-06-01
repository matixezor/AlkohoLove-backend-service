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
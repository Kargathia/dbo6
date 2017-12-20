db = new Mongo().getDB('spells');

db.spells.find(
    {
        $and: [
            { area: { $exists: true } },
            { target: { $exists: true } }
        ]
    }
).forEach(item => printjson([item.target, item.area]));

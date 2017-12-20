db = new Mongo().getDB('spells');

// Note: because we need to access the table through 'this', we can't use fat arrow notation in the anonymous functions
res = db.spells.mapReduce(
    function() { for (var key in this) { emit(key, null); } },
    function(key, stuff) { return null; },
    { out: 'distinct_keys' }
)

// List of all distinct keys in database
dist_list = db.distinct_keys
.distinct('_id');

// List of dicts: key = distinct db key, val = '{ $exists: false }'
// can be used in queries
selector = dist_list
.map((item) => { ret = {}; ret[item] = { $exists: false }; return ret});

// find all spells that are missing at least one key
res = db.spells
.find({$or: selector})
// filter through values, return a new item listing title + missing keys
.map(item => { 
    return {
        title: item.title, 
        missing: dist_list.filter(k => (!(k in item)))
    };
})
.forEach(printjson)
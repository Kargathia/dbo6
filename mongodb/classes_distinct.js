db = new Mongo().getDB('spells');

// Note: because we need to access the table through 'this', we can't use fat arrow notation in the anonymous functions
res = db.spells.mapReduce(
    function() { for (var key in this.levels) { emit(key, null); } }, // we only want the key (== class name)
    function(key, stuff) { return null; },
    { out: 'spell_classes' }
)

db.spell_classes
.distinct('_id')
.forEach(printjson);

db = new Mongo().getDB('spells');

// Note: because we need to access the document through 'this', we can't use fat arrow notation in the anonymous functions
res = db.spells.mapReduce(
    function() { for (var key in this.levels) { emit(key, null); } }, // we only want the key (== class name)
    function(key, stuff) { return null; }, // we're not interested in any of the values
    { out: 'spell_classes' } // created collection with output
);

db.spell_classes
.distinct('_id')
.forEach(printjson);

db = new Mongo().getDB('spells');

db.spells
.find({ 'target': { $exists: false }, 'range': { $exists: false } })
.forEach((item) => printjson(item));

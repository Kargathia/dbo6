db = new Mongo().getDB('spells');

db.spells
.find({ 'levels.wizard': { $lt: 4 } })
.sort({ title: 1 })
.forEach(item => printjson(item.title));

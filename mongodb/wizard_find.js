db = new Mongo().getDB('spells');

db.spells
.find({ 'levels.wizard': 3 })
.sort({ title: -1 })
.forEach((item) => printjson(item.title));

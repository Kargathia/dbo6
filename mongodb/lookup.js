db = new Mongo().getDB('spells');

db.spells
.find({ 'title': { $regex: '^ray of enfeeblement', $options: 'i'} })
.forEach(item => printjson(item));
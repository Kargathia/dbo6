db = new Mongo().getDB('spells');

db.spells
.find(
    { 'school': { $regex: '^conjuration', $options: 'i'} },
    { _id: 0, title: 1, school: 1}
)
.sort({ title: 1 })
.forEach(printjson);

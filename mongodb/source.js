db = new Mongo().getDB('spells');

db.spells
    .find({ url: { $regex: '^.+?/prd/([^/]+)/'} })
    .forEach(doc => {
        doc.source = doc.url.match('^.+?/prd/([^/]+)/')[1]
        db.spells.save(doc);
    });

db.spells
    .find()
    .forEach(doc => printjson([doc.title, doc.source]))

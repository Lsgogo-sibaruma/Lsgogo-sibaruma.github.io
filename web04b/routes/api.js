var express = require('express');
var router = express.Router();

sqlite = require('sqlite3').verbose();
db = new sqlite.Database("./db.sqlite", sqlite.OPEN_READWRITE, (err) => {
    if (err) {
        console.error(err.message);
    }
    console.log('Connected to the database.');
});

/* GET home page. */
router.get('/', function(req, res, next) {
    sql= "SELECT * FROM vga";
    db.all(sql, [], (err, rows) => {
        if (err) {
            throw err;
        }
        res.send(rows);
    });
});


router.post('/', (req, res) => {
    const {time, item, price}=req.body;
    sql = "INSERT INTO vga (time, item, price) VALUES (?, ?, ?)";
    db.run(sql, [time, item, price], (err) => {
        if (err) {
            console.error(err.message);
            return res.status(500).send(err.message);
        }
        console.log('inserted');
    });
    //res.redirect('/data.html');
    return res.status(200).send('inserted');
})

module.exports = router;
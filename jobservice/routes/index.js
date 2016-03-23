var express = require('express');
var router = express.Router();
var util = require('util');
/* GET home page. */
router.get('/', function(req, res, next) {
    console.log(req.query);
    console.log(req.body);
    res.render('index', { title: 'Express' });
});


router.post('/', function(req, res, next) {
    console.log(util.inspect(req,false, null));
    //console.log(req.body);
    console.log(req.query);
    res.render('index', { title: 'Express' });
});



module.exports = router;

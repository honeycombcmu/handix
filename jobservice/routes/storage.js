/**
 * Created by handixu on 3/21/16.
 */
var express = require('express');
var router = express.Router();
var localDir = "/Users/handixu/Documents/honeycomb/handix/jobservice"
const exec = require('child_process').exec;
var multer = require('multer');
/* GET home page. */

var storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, localDir + '/' + req.query.user);
    },
    filename: function (req, file, cb) {
        cb(null, req.query.filename); //Appending .jpg
    }
})
router.use(function(req, res, next) {

    // log each request to the console
    console.log(req.method, req.url);
    console.log(req.body);
    

    // continue doing what we were doing and go to the route
    next();
});

router.post('/put', multer({storage: storage}).single('data'), function(req, res, next) {
    console.log("hahahahaha");
    var cmd = 'HADOOP_USER_NAME=hdfs hdfs dfs -put ';
    var user = req.query.user;
    var filename = req.query.filename;
    var filepath = '/user/spark/' +user + 'input/' +filename;
    var local = localDir + user+ filename;
    cmd += ' ' + localDir + '/' + user + '/' + filename;
    cmd += ' ' + filepath;
    console.log(cmd);

    exec(cmd, function(err, stdout, stderr){
        //TODO: change status of the job
        if (err) {
            console.error(err);
            return;
        }
        console.log(stdout);
    });

    //console.log(req.body.status);
    //console.log(JSON.parse(req.body));
    //console.log("algorithm="+req.query.algorithm);

    res.render('index', { title: 'Express' });
});

module.exports = router;
/**
 * Created by handixu on 3/21/16.
 */
var express = require('express');
var router = express.Router();
const exec = require('child_process').exec;

/* GET home page. */

router.use(function(req, res, next) {

    // log each request to the console
    console.log(req.method, req.url);

    // continue doing what we were doing and go to the route
    next();
});

router.post('/', function(req, res, next) {
    cmd = 'HADOOP_USER_NAME=hdfs /bin/spark-submit /home/honeycomb/SparkTeam/PySpark.py ';
    cmd += req.body.traindata+ ' ' + req.body.testdata + ' '+ req.body.outpath;
    exec('my.bat', function(err, stdout, stderr){
        //TODO: change status of the job
        if (err) {
            console.error(err);
            return;
        }
        console.log(stdout);
     });
    //console.log(req.body.status);
    //console.log(JSON.parse(req.body));
    console.log("algorithm="+req.query.algorithm);

    res.render('index', { title: 'Express' });
});

module.exports = router;
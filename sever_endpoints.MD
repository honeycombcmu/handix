
Endpoint for start a new job:<br/>
  <ip>:<port>/jobs?algorithm=<algorithm_name>
  Example usage: 
    curl --data-binary @my-job-config.json 'localhost:8090/jobs?algorithm=knn'
    
  example result:
  {
   "status": "STARTED",
   "result": {
    "jobId": "122312-adfsasdf-123213-qewq-wqeqw121211",
    "algorithm": "knn"
    "config": "my-job-config.json"
    }
  }
    
    
Endpoint for check status of a job:
    <ip>:<port>/jobs/<job-id>
    Example usage: 
      curl 'localhost:8090/jobs/122312-adfsasdf-123213-qewq-wqeqw121211'  
    example result:
    {
     "duration": "6.341 secs",
     "startTime": "2016-02-20T00:00:00.000Z",
     "algorithm": "knn",
     "result": {}
  "status": "Started",
  "jobId": "122312-adfsasdf-123213-qewq-wqeqw121211"
}
    
    
    

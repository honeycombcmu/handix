###              RFC-HoneyFS

####Goal

Simplify file upload/download for front-end.
Provide more file manipulation operations for front-end.

####Background
Currently, when a file is uploaded from front-end, a script need to be ran to put that file into HDFS. Front-end cannot check the file directory in backend file system.
 
####Overview
Framework: Python Flask

File System: TBD, should be easily replaceable 
 

####Run book
```
git clone git@github.com:honeycombcmu/handix.git

cd honeyfs

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python app.py
```

Week 1: 

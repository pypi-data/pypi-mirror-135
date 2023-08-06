# python-bsc
This is a python package containing a basic implementation of the Balanced Scorecard as designed by Kaplan and Norton. It is currently geared for agriculture but can be altered to fit any organisational need

## Implementation
The current implementation is a mix of _sqlalchemy_ on the database side and _flask_ mixed with some bootstrap and _wtf_ _forms_. 
The database can be spun up with a few commands as explained in more detail lower down, and the UI generated via _flask_ can be used 
to populate the tables within the database. 

Additions are relatively straight forward and so this package can be altered to suit a multitude of organisational needs
with some adjustments, even if the stack is the only thing used. 

## Features
* sqlalchemy back end
* Example implementation for an agrilcultural company
* Implements the Balanced Scorecard with objectives and measures
* Can be run in a dockerised environment

## Requirements
* Linux or Mac (windows not yet supported)
* Docker
* Postgresql client or just a psql docker container

To run and use this code base you need database backend where the tables can be built. 
I suggest running a postgresql docker container, but any standard sql contianer should work with some minor adjustments. 
See the section on starting a docker container with postgresql.

## Getting started
Create a virtual environment
```
python3 virtualenv <name-your-env>
source <name-your-env>/bin/activate
```

Install the package
```commandline
pip install python-bsc
```



## Running a postgresql docker container

```commandline
docker run -d --name my-bsc-db -e POSTGRES_HOST_AUTH_METHOD=trust -v my_dbdata:/var/lib/postgresql/bsc-data -p 5432:5432 postgres:12
```
## Contributing
Clone the repo
```commandline
git clone 
```
## Issues
I am super amped to improve this package and learn from the community. If you a suggestions or an improvement
let me know or send those requests, I will do my best. 
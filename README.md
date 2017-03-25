# PYEJ

PYEJ is a online judge in python made to be descentralized and safe.

## How to Run

### Setting up Environment:

requirements:

* python >= 3.6
* rabbitmq-server running

You should start by creating a virtual environment to work on:

`mkvirtualenv --python=python3.6 pyej`  
`pip install pika`  
`pip install pony`  

You will need a config file placed in `/opt/pyej/config.ini` that should look like this:

[rabbitmq]  
JUDGE_XCH = xch_topic_pyej

[db]  
user = \<user\>  
password = \<password\>  
name = pyej_dev  

A database called *pyej_dev* is required on postgres, it can be created with:

`sudo -u postgres psql`  
`CREATE DATABASE pyej_dev;`  

Now the database can be populated with a dummy problem running `./admin create`, to see if it worked propoerly you can run `./admin read`

### Running:

To run PYEJ its needed to run 3 sub-modules:

* Judge: Compile, execute and gives a veredict  
The host (--host) and the language (-l or --language) have to be specified. ex: `./judge.py --host localhost -l cpp`
* Courier: Get messages about the problems judged to handle extern consumers (Scoreboards, Database, ...)  
Can be run simple with `./courier.py`
* Client: Sends a submission of a problem  
The host (--host), the language (-l or --language), the file (-f or --file), the user (-u or --user) and the problem (-p or --problem) have to be specified. `./client.py -l cpp --host localhost -f ./test_code_cpp.cpp -u 1 -p 1`

### Running the tests:

nosetests -sv ./tests/*.py  

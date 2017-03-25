# BROJ (BR Online Judge)

BROJ is an implementation of a fault tolerant electronic judge capable of withstanding large processing loads. Designed for application on educational contexts that require mass grading, such as programming competitions.  

## Setting up the environment:

Requirements:
* Python >= 3.6
* RabbitMQ-server

You should start by [creating a virtual environment](https://virtualenvwrapper.readthedocs.io/) to work on:  
```sh
$ mkvirtualenv --python=python3.6 broj
$ pip install -r requirements.txt
```

You will need a config file placed in `/opt/broj/config.ini` that should look like this:  
```ini
[db]
user = <user>
password = <password>
name = broj_dev
```

A database called **broj_dev** is required on postgres, it can be created with:  
```sh
$ sudo -u postgres psql
$ CREATE DATABASE broj_dev;
```

Now the database can be populated with a dummy problem running by `./admin.py create`. To check the database run `./admin.py read`.  

## Running:

##### Client
```sh
./client.py -l cpp -f ./test_code_cpp.cpp -u 1 -p 1
```

##### Judge
```sh
./judge.py -l cpp
```

##### Courier
```sh
./courier.py
```

## Running the tests:
```sh
./runtests.sh
```

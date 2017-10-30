# BROJ (BR Online Judge)

[![Build Status](https://travis-ci.org/BROnlineJudge/broj.svg?branch=master)](https://travis-ci.org/BROnlineJudge/broj)
[![codecov](https://codecov.io/gh/BROnlineJudge/broj/branch/master/graph/badge.svg)](https://codecov.io/gh/BROnlineJudge/broj)

BROJ is an implementation of a fault tolerant electronic judge capable of withstanding large processing loads. Designed for application on educational contexts that require mass grading, such as programming competitions.  

## Setting up the environment:

Requirements:
* Python >= 3.6
* RabbitMQ-server

You should start by [creating a virtual environment](https://virtualenvwrapper.readthedocs.io/) to work on:  
```sh
$ mkvirtualenv --python=/usr/bin/python3.6 broj
$ pip install -r requirements.txt
```

You will need a local config file `config.ini` that should look like this:  
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
Create the database admin user:
```sh
$ sudo -u postgres createuser <username>
$ sudo -u postgres psql
alter user <username> with encrypted password '<password>';
grant all privileges on database <dbname> to <username> ;
```

Now the database can be populated with a dummy problem running by `./admin.py create`. To check the database run `./admin.py read`.  

If you have any trouble with locales, use the command

$ sudo dpkg-reconfigure locales

and select 'pt_BR.UTF-8' as the default locale.

## Running:

##### Judge
```sh
./judge.py -l cpp
```

##### Client
```sh
./client.py -l cpp -f ./solutions/1.cpp -u localhost -p "Dia da Vovó"
```

##### Courier
```sh
./courier.py
```

## Running the tests:
```sh
./runtests.sh
```

## Custom Check Output

It's possible to write your own output checker instead of just a simple diff, and its very simple, you just need to define the method `check` that will receive 3 string parameters: the input, expected output and user output of the test case, respectively.  

Here you can see a simple check if the output is the input divided by 2 with custom precision:
```python
def check(input, output, user_output):
    import io
    inbuf = io.StringIO(input)
    a = float(inbuf.read())
    outbuf = io.StringIO(user_output)
    b = float(outbuf.read())
    return (abs(a/2.0 - b) < 1e-6)
```

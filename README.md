# BROJ (BR Online Judge)

[![Build Status](https://travis-ci.org/BROnlineJudge/broj.svg?branch=master)](https://travis-ci.org/BROnlineJudge/broj)
[![codecov](https://codecov.io/gh/BROnlineJudge/broj/branch/master/graph/badge.svg)](https://codecov.io/gh/BROnlineJudge/broj)

BROJ is an implementation of a fault tolerant electronic judge capable of withstanding large processing loads. Designed for application on educational contexts that require mass grading, such as programming competitions.  

## Setting up the environment:

Requirements:
* vagrant + virtualbox

```sh
$ vagrant up
$ vagrant ssh
# Populate the DB with the dummy problems
$ ./admin.py create
$ ./admin.py read
```

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

## Custom Check Output

It's possible to write your own output checker instead of just a simple diff, and its very simple. You just need to define the method `check` that will receive 3 string parameters: the input, expected output and user output of the test case, respectively.  

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

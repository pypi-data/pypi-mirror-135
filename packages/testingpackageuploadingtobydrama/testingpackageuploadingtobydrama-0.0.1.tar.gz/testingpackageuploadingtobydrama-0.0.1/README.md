# Hello World
This is an example projeckt demonstarting how to publish a python module to PyPI.

##Installation
run the following to install:
```python
pip install helloworld
```

##Usage
```python
from helloworld import say_hello

#Generate "Hello, world!"
say_hello()

#Generate "Hello, everybody!"
say_hello("Everybody")
```
# Developing Hello World
To install helloworld, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
pip install -e .[dev]
```
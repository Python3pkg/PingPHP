#!/bin/bash

pip install -r requirements.txt

python setup.py sdist

pip install dist/*.tar.gz

cd ./test

pingrun







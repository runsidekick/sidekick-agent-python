#!/bin/bash

set -e
set -x

pip install wheel
python setup.py sdist bdist_wheel

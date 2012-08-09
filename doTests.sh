#!/bin/sh
cd src
python -m unittest discover -p "*Test.py" -s ../tests/
cd ..

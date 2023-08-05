#!/bin/zsh

sudo rm -f dist/*
sudo python3 setup.py bdist_wheel
sudo python3 setup.py sdist --formats=gztar
twine upload dist/*
#twine upload dist/*whl

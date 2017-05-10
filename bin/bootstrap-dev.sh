#!/bin/bash

# Extra packages
yum -y install git
yum -y install gcc
yum -y install python-devel

# upgrade pip
yum -y install python2-pip
pip install --upgrade pip

# st2sdk
yum -y install libyaml libyaml-devel
pip install PyYAML
pip install st2sdk

# cookiecutter
pip install --upgrade cookiecutter

# ipython
pip install ipython

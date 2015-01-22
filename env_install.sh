#!/bin/bash

yum -y groupinstall "Development tools"
yum -y install gcc zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel git

curl -O https://www.python.org/ftp/python/3.4.2/Python-3.4.2.tgz

tar zxf Python-3.4.2.tgz

cd Python-3.4.2
./configure --prefix=/opt/local
make && make altinstall

curl -kL https://bootstrap.pypa.io/get-pip.py | /opt/local/bin/python3.4

/opt/local/bin/pip install -U setuptools
/opt/local/bin/pip install twitter
/opt/local/bin/pip install python-daemon

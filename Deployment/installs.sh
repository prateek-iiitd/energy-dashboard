#!/bin/sh

apt-get update
apt-get install git -y
apt-get install python-pip -y
apt-get install python-dev -y
apt-get install python-numpy -y
apt-get install python-scipy -y
sudo apt-get install libffi-dev
pip install pyOpenSSL
apt-get install libcurl4-gnutls-dev librtmp-dev -y
pip install pycURL
pip install pymodbus
sudo pip install zope.interface twisted python-dateutil avro configobj
git clone https://bitbucket.org/zenatix/smap
cd smap/python
sudo setup.py install

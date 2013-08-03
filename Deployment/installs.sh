#!/bin/sh

apt-get update
apt-get install python-pip -y
apt-get install python-dev -y
apt-get install python-numpy -y
apt-get install python-scipy -y
pip install smap
pip install pyOpenSSL
apt-get install libcurl4-gnutls-dev librtmp-dev -y
pip install pycURL
pip install pymodbus

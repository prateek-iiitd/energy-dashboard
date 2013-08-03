#!/bin/bash

echo "1"
for dest in $(<all-ip.txt); do
	echo "2"
	ssh -p 1234 pi@${dest} sudo chmod 777 -R /usr/local/lib/python2.7/dist-packages/smap/drivers
done

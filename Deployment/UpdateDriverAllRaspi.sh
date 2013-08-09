#!/bin/bash

for dest in $(<IP-List.txt); do
	echo "Updating driver on ${dest}"
	scp -P 1234 modbus_usb.py pi@${dest}:/usr/local/lib/python2.7/dist-packages/smap/drivers/.
done

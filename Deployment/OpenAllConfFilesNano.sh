#!/bin/bash

for dest in $(<IP-List.txt); do
	ssh -t -p 1234 pi@${dest} "cd /home/pi/smap; nano *.conf"
done

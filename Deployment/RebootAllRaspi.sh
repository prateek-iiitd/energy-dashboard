#!/bin/bash

for dest in $(<all-ip.txt); do
	echo "Rebooting RasPi at ${dest}"
	ssh -p 1234 pi@${dest} sudo reboot
done

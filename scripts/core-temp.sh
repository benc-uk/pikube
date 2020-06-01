#!/bin/bash

echo -e "🌡 master" && ssh pi@master vcgencmd measure_temp
echo -e "\n🌡 node-1" && ssh pi@node-1 vcgencmd measure_temp
echo -e "\n🌡 node-2" && ssh pi@node-2 vcgencmd measure_temp
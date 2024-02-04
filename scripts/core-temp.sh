#!/bin/bash

echo -e "🌡 master" && ssh master vcgencmd measure_temp
echo -e "\n🌡 node-1" && ssh node1 vcgencmd measure_temp
echo -e "\n🌡 node-2" && ssh node2 vcgencmd measure_temp

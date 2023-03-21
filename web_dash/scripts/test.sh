#!/bin/bash
VALUE=$(ifconfig wlan1 | grep -i inet)

if ["$VALUE"];
then
	echo "Failed to connect to ${WIFI_SSID}"
else
	echo "Connected to ${WIFI_SSID}"
fi

echo $(ifconfig wlan1 | grep -i inet)
exit 0

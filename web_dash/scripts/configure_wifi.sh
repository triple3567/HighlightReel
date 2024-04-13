#!/bin/bash

# TODO
# 1. Set up env variabled for wifi config
# 2. configure connamnctl trough /var/lib/connman settings file
# 3. restart connmanctl service
# 4. ensure wifi is connected 

#if [[ $(/usr/bin/id -u) -ne 0 ]]; then
#	echo "Please run as root"
#	exit 1
#fi

WIFI_SSID=$1
WIFI_PSK=$2

if [ -z "$WIFI_SSID" ]; then
	echo "\$WIFI_SSID Env variable is empty"
	exit 1
fi

if [ -z "$WIFI_PSK" ]; then
	echo "\$WIFI_PSK Env variable is empy"
	exit 1
fi 

LOGFILE=wifi_setup.log
date >> $LOGFILE
printf "SSID: ${WIFI_SSID}\nPSK: ${WIFI_PSK}\n" >> $LOGFILE

NETWORK_FILE="/etc/wpa_supplicant/wpa_supplicant-wlan1.conf"
#NETWORK_FILE="/home/pi/HighlightReel/scripts/test.conf"

printf "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n" > $NETWORK_FILE
printf "update_config=1\n" >> $NETWORK_FILE
printf "network={\n" >> $NETWORK_FILE
printf "\tssid=\"${WIFI_SSID}\"\n" >> $NETWORK_FILE
printf "\tpsk=\"${WIFI_PSK}\"\n" >> $NETWORK_FILE
printf "}\n" >> $NETWORK_FILE

sudo /usr/sbin/wpa_supplicant -B -iwlan1 -c /etc/wpa_supplicant/wpa_supplicant-wlan1.conf -D nl80211 -D wext || true

wpa_cli -i wlan1 reconfigure
/usr/sbin/ip link set wlan1 up
sleep 30

echo "Connected to ${WIFI_SSID}"

exit 0

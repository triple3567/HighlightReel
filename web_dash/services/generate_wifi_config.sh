#!/bin/bash

#file=test.conf
file=/etc/hostapd/hostapd.conf

rm -f $file
touch $file

echo "interface=wlan0" >> $file
echo "driver=nl80211" >> $file
echo "ssid=HighlightReel_$(cat /sys/firmware/devicetree/base/serial-number)" >> $file
echo "hw_mode=g" >> $file
echo "channel=6" >> $file
echo "ieee80211n=1" >> $file
echo "wmm_enabled=1" >> $file
echo "auth_algs=1" >> $file
echo "ignore_broadcast_ssid=0" >> $file
echo "wpa=2" >> $file
echo "wpa_key_mgmt=WPA-PSK" >> $file
echo "wpa_passphrase=HighlightReelAdmin" >> $file
echo "rsn_pairwise=CCMP" >> $file

systemctl start hostapd

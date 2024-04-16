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

systemctl restart hostapd

hexchars="0123456789abcdef"
end=$( for i in {1..6} ; do echo -n ${hexchars:$(( $RANDOM % 16 )):1} ; done | sed -e 's/\(..\)/:\1/g' )
MAC_ADDR=00:60:2F$end
sudo ip link set wlan1 down
sudo ip link set wlan1 address $MAC_ADDR
sudo ip link set wlan1 up
sudo wpa_supplicant -B -iwlan1 -c /etc/wpa_supplicant/wpa_supplicant-wlan1.conf -Dnl80211,wext || true

echo "successful wifi-config setup"

exit 0

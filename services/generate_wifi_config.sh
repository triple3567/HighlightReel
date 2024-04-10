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

MAC_ADDR=$(hexdump -n 6 -ve '1/1 "%.2x "' /dev/random | awk -v a="2,6,a,e" -v r="$RANDOM" 'BEGIN{srand(r);}NR==1{split(a,b,",");r=int(rand()*4+1);printf "%s%s:%s:%s:%s:%s:%s\n",substr($1,0,1),b[r],$2,$3,$4,$5,$6}')
sudo ip link set wlan1 down
sudo ip link set wlan1 address $MAC_ADDR
sudo ip link set wlan1 up
sudo wpa_supplicant -B -iwlan1 -c /etc/wpa_supplicant/wpa_supplicant-wlan1.conf -Dnl80211,wext || true

echo "successful wifi-config setup"

exit 0

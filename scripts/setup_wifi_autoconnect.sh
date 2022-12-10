# TODO
# 1. Set up env variabled for wifi config
# 2. configure connamnctl trough /var/lib/connman settings file
# 3. restart connmanctl service
# 4. ensure wifi is connected 

WIFI_SSID=$PWD
echo $WIFI_SSID
connmanctl enable wifi
connmanctl agent on
connmanctl scan wifi
echo done
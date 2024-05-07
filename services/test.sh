#!/bin/bash
hexchars="0123456789ABCDEF"
end=$( for i in {1..10} ; do echo -n ${hexchars:$(( $RANDOM % 16 )):1} ; done | sed -e 's/\(..\)/:\1/g' )
MAC_ADDR=32$end
echo $MAC_ADDR

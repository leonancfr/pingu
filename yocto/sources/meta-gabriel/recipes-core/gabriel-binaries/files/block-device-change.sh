#!/bin/bash

echo "blk-dev-change $$: Device $1 change. Running block-device-attach" >> /dev/kmsg

/opt/gabriel/bin/block-device-attach.sh $1
#!/bin/bash

DEVICE="$1"

# Check if the device is mounted
if grep -qs "^/dev/${DEVICE}[0-9]*" /proc/mounts; then
  # Unmount all partitions of the device
  umount /dev/${DEVICE}[0-9]*

  # Print success message
  echo "All partitions of /dev/${DEVICE} were unmounted successfully."
else
  # Print error message
  echo "/dev/${DEVICE} is not mounted."
fi

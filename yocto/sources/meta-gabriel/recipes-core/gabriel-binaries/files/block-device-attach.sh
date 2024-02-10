#!/bin/bash

# This function adds a new line to the fstab file with the specified UUID, mount point, and partition type.
# Arguments:
#   $1: UUID of the partition to be mounted
#   $2: partition type (e.g. exfat, ext4, etc.)
insert_uuid_into_fstab () {
	  # Check if /media/usb0 already exists in /etc/fstab
  if grep -q "/media/usb0" /etc/fstab; then
    echo -e "blk-dev-attach $$: \t\tRemoving existing entry for /media/usb0 in /etc/fstab" >> /dev/kmsg
    sed -i '/\/media\/usb0/d' /etc/fstab
  fi

  # Add new line to /etc/fstab
  echo -e "blk-dev-attach $$: \t\tAdding a new entry for UUID $1 in /etc/fstab" >> /dev/kmsg
  echo -e "UUID=$1\t/media/usb0\tauto\tdefaults,rw,user,sync,auto,exec,noatime,nodiratime,nofail\t0\t2" | tee -a /etc/fstab > /dev/null
  #defaults,rw,user,sync,auto,exec,noatime,nodiratime,nofail
}

# This function checks if a given UUID exists in /etc/fstab file
# Arguments:
#	$1: UUID to check if exists
# Return
# 	0 if exists
# 	1 if not exists
uuid_exists_in_fstab(){
	uuid="$1"
	grep -q "UUID=$uuid" /etc/fstab
	if [[ $? -eq 0 ]]; then
		return 0
	else
		return 1
	fi
}

# Formats a disk to exFAT with a new partition of the same size as the disk
# Arguments:
# 	$1: device path (/dev/sdx1)
# Check if the disk is already partitioned
format_disk_to_exfat() {
    local disk=$1
    echo -e "blk-dev-attach $$: \t\tFormatting disk ${disk}" >> /dev/kmsg

    # Format the disk to exFAT with a default label
    if mkfs.exfat -n "GabrielHD" "$1" > /dev/null; then
        echo -e "blk-dev-attach $$: \t\t\tDisk formated." >> /dev/kmsg
    else
        echo -e "blk-dev-attach $$: \t\t\tError: Failed to format disk." >> /dev/kmsg
        return 1
    fi
    
    echo -e "blk-dev-attach $$: \t\tConfigure partition table of disk $disk to GPT." >> /dev/kmsg
    if parted -s $disk mklabel gpt; then
        echo -e "blk-dev-attach $$: \t\t\tOK" >> /dev/kmsg
    else
        echo -e "blk-dev-attach $$: \t\t\tERROR" >> /dev/kmsg
        return 1
    fi

    echo -e "blk-dev-attach $$: \t\tFormat disk to use entire disk size" >> /dev/kmsg
    if parted -s $disk mkpart primary 0% 100%; then
        echo -e "blk-dev-attach $$: \t\t\tOK" >> /dev/kmsg
    else
        echo -e "blk-dev-attach $$: \t\t\tERROR" >> /dev/kmsg
        return 1
    fi

    # Format the partition with exFAT and a custom label
    echo -e "blk-dev-attach $$: \t\tFormatting partition ${disk}1 with exFAT" >> /dev/kmsg
    if mkfs.exfat -n "gabriel" $disk"1" > /dev/null; then
        echo -e "blk-dev-attach $$: \t\t\tOK" >> /dev/kmsg
    else
        echo -e "blk-dev-attach $$: \t\t\tError" >> /dev/kmsg
        return 1
    fi

    echo -e "blk-dev-attach $$: \t\tSuccessfully formatted ${disk} with exFAT" >> /dev/kmsg
    return 0
}


# Restarts the history container if it's currently running
restart_history_container() {
    echo -e "blk-dev-attach $$: Checking if docker is running" >> /dev/kmsg
    # Check if Docker is running
    CHECK_IF_DOCKER_IS_UP="$(systemctl --type=service | grep docker.service | awk '{print $3,$4}')"

    if [ "$CHECK_IF_DOCKER_IS_UP" == "active running" ]; then
        echo -e "blk-dev-attach $$: \tDocker is running. Checking if history container is running" >> /dev/kmsg
        history_is_running="$(docker ps -f name=history -q)"
        if [ ! -z "$history_is_running" ]; then
            echo -e "blk-dev-attach $$: \t\tRestarting history container." >> /dev/kmsg
            docker restart $history_is_running 
        else 
            echo -e "blk-dev-attach $$: \t\tHistory container is not running." >> /dev/kmsg
        fi
    else
        echo -e "blk-dev-attach $$: \tDocker is not running yet." >> /dev/kmsg
    fi
}

# Restarts the device-monitor container if it's currently running
restart_device_monitor_container() {
    echo -e "usb-attach $$: Checking if docker is running" >> /dev/kmsg
    # Check if Docker is running
    CHECK_IF_DOCKER_IS_UP="$(systemctl --type=service | grep docker.service | awk '{print $3,$4}')"

    if [ "$CHECK_IF_DOCKER_IS_UP" == "active running" ]; then
        echo -e "usb-attach $$: \tDocker is running. Checking if device-monitor container is running" >> /dev/kmsg
        device_monitor_is_running="$(docker ps -f name=device-monitor -q)"
        if [ ! -z "$device_monitor_is_running" ]; then
            echo -e "usb-attach $$: \t\tRestarting device-monitor container." >> /dev/kmsg
            docker restart device-monitor 
        else 
            echo -e "usb-attach $$: \t\Device-monitor container is not running." >> /dev/kmsg
        fi
    else
        echo -e "usb-attach $$: \tDocker is not running yet." >> /dev/kmsg
    fi
}

# Get the number of partitions of a disk
get_num_partitions () {
  disk="$1"
  partitions=$(parted -m $disk print | grep -c '^[0-9].*:')
  echo "$partitions"
}

# Mounts all partitions on a removable media device
# Usage: mount_removable_media <device_path>
function mount_removable_media() {
    # Check if device path is provided as an argument
    if [ -z "$1" ]; then
        echo "blk-dev-attach $$: \tError: no device path provided" >> /dev/kmsg
        return 1
    fi

    # Extract device name from device path
    device=$(basename "$1")

    # Get a list of all partitions on the device
    partitions=($(ls -1 /dev/${device}* | grep -v "${device}$"))

    # Check if no partitions are found on the device
    if [ ${#partitions[@]} -eq 0 ]; then
        echo "blk-dev-attach $$: \tNo partitions were found on the device." >> /dev/kmsg
        return 1
    fi

    # Mount each partition into a directory under /media/rmvb
    for partition in "${partitions[@]}"; do
        mount_point="/media/rmvb/$(basename ${partition})"
        echo -e "blk-dev-attach $$: \tMounting partition $partition into $mount_point" >> /dev/kmsg
        
        # Create mount point directory if it doesn't exist
        if ! mkdir -p $mount_point; then
            echo "blk-dev-attach $$: \t\tFailed to create mount point directory: $mount_point" >> /dev/kmsg
            return 1
        fi
        
        # Mount partition
        if ! mount $partition $mount_point; then
            echo "blk-dev-attach $$: \t\tFailed to mount partition: $partition" >> /dev/kmsg
            return 1
        fi
    done
}

create_mount_point() {
  local mount_point=$1
  if [[ ! -d "$mount_point" ]]; then
    echo -e "blk-dev-attach $$: \tCreating mount point $mount_point..."  >> /dev/kmsg
    mkdir -p "$mount_point"
  fi
}

# Função que monta a partição no ponto de montagem
mount_partition() {
  local mount_point="/media/check_hd"
  echo -e "blk-dev-attach $$: \tMounting partition $1 on $mount_point..."  >> /dev/kmsg
  if mount "$1" "$mount_point"; then
    echo -e "blk-dev-attach $$: \t\tMount successful."  >> /dev/kmsg
    return 0
  else
    echo -e "blk-dev-attach $$: \t\tMount failed."  >> /dev/kmsg
    return 1
  fi
}

# Função que verifica se o diretório de upload existe na partição montada
check_upload_directory() {
  local mount_point="/media/check_hd"
  if [[ -d "$mount_point/uploader_folder" ]]; then
    echo -e "blk-dev-attach $$: \tDirectory uploader_folder found."  >> /dev/kmsg
    return 0
  else
    echo -e "blk-dev-attach $$: \tDirectory uploader_folder not found."  >> /dev/kmsg
    return 1
  fi
}

# Função que desmonta a partição e remove o ponto de montagem
cleanup() {
  local mount_point="/media/check_hd"
  echo -e "blk-dev-attach $$: \t\tUnmounting partition..."  >> /dev/kmsg
  umount "$mount_point"
  echo -e "blk-dev-attach $$: \t\tRemoving mount point $mount_point..."  >> /dev/kmsg
  rmdir "$mount_point"
}

# Função principal que chama as outras funções e retorna o resultado
disk_is_empty () {
  # Verifica se um argumento foi passado para a função
  if [[ -z "$1" ]]; then
    echo -e "blk-dev-attach $$: \tAn argument is required for this function."  >> /dev/kmsg
    return 1
  fi
  umount $1 
  create_mount_point "/media/check_hd"
  if ! mount_partition "$1"; then
    echo -e "blk-dev-attach $$: \tMount failed. Returning as if directory is full."  >> /dev/kmsg
    cleanup
    return 1
  fi
  if check_upload_directory; then
    cleanup
    return 1
  else
    cleanup
    return 0
  fi
}


echo -e "blk-dev-attach $$: A disk was inserted!" >> /dev/kmsg

LOCKFILE="/tmp/gabriel_hd.lock"

# Check if lock file exists
if [ -f "$LOCKFILE" ]; then
    echo "blk-dev-attach $$: Aborting old script..." >> /dev/kmsg
    # mata todos os processos associados ao lock
    parent_pid=$(cat $LOCKFILE)
    child_pids=$(pgrep -P $parent_pid)
    child_pids+=" $parent_pid" 

    echo "blk-dev-attach $$: Aborting pids $child_pids" >> /dev/kmsg

    for pid in $child_pids; do
        kill -9 $pid
    done
    # Remove lock file
    rm "$LOCKFILE"
fi

# Create lock file
echo "$$" > "$LOCKFILE"

create_mount_point "/media/usb0"

dev_disk="/dev/$1"

disk_size=$(($(lsblk -b --output SIZE -n -d $dev_disk) / 1024 / 1024 / 1024))

if [ $disk_size -lt 900 ]; then
    if [ $disk_size -gt 0 ]; then
        echo -e "blk-dev-attach $$: The disk size is less than 900GB.\nThe device will be mounted as a removable media." >> /dev/kmsg
        mount_removable_media $dev_disk
    else
        echo "blk-dev-attach $$: === - Ghost Disk - ===" >> /dev/kmsg
        restart_history_container
        restart_device_monitor_container
    fi
    echo "blk-dev-attach $$: Success"  >> /dev/kmsg
    rm -f "$LOCKFILE"
    exit 0
fi

echo -e "blk-dev-attach $$: Checking disk" >> /dev/kmsg
if [ $(get_num_partitions "$dev_disk") -eq 0 ]; then
    echo -e "blk-dev-attach $$: \tDrive without partitions. The disk will be formated." >> /dev/kmsg
    format_disk_to_exfat $dev_disk
fi

dev_part=$dev_disk"1"
echo -e "blk-dev-attach $$: Checking partitions" >> /dev/kmsg
disk_format=$(lsblk -o FSTYPE -n $dev_part)
echo -e "blk-dev-attach $$: \tPartition type: $disk_format" >> /dev/kmsg
if ! ( [ "$disk_format" == "exfat" ] || [ "$disk_format" == "ext4" ] ) && [ "$disk_format" != "" ] ; then
    echo -e "blk-dev-attach $$: \tDrive with unsupported format. The disk will be formated." >> /dev/kmsg
    format_disk_to_exfat $dev_disk
fi


UUID=$(blkid -s UUID -o value $dev_part) 

uuid_exists_in_fstab "$UUID"
if [ $? -eq 1 ]; then
    echo -e "blk-dev-attach $$: \tUUID not present in fstab, checking if disk have videos" >> /dev/kmsg
    disk_is_empty "$dev_part"
    if [ $? -eq 0 ]; then
        disk_format=$(lsblk -o FSTYPE -n $dev_part)
        if [ "$disk_format" != "exfat" ] &&  [ "$disk_format" != "" ] ; then
            echo -e "blk-dev-attach $$: \tHard drive is empty. The disk will be formated." >> /dev/kmsg
            format_disk_to_exfat $dev_disk
        else
            echo -e "blk-dev-attach $$: \tHard drive is empty and formated in exfat." >> /dev/kmsg
        fi
    fi
fi

UUID=$(blkid -s UUID -o value $dev_part) 
disk_format=$(lsblk -o FSTYPE -n $dev_part)
echo -e "blk-dev-attach $$: Inserting partition in fstab if it does not exist:" >> /dev/kmsg
echo -e "blk-dev-attach $$: \tUUID: $UUID" >> /dev/kmsg
echo -e "blk-dev-attach $$: \tFormat: $disk_format"  >> /dev/kmsg
insert_uuid_into_fstab $UUID $disk_format

echo -e "blk-dev-attach $$: Recovering corrupted data, if any." >> /dev/kmsg
if [ "$disk_format" == "exfat" ]; then
    fsck.exfat -y "$dev_part"
else
    fsck -y "$dev_part"
fi

# Checks if a device is mounted at /media/usb0. 
# If it is not, then it mounts the device at /media/usb0.
echo -e "blk-dev-attach $$: Checking if external drive is already mounted" >> /dev/kmsg
if ! mount | grep "$dev_part.*on /media/usb0" > /dev/null; then
    echo -e "blk-dev-attach $$: \tDevice $dev_part will be mounted" >> /dev/kmsg
    if mount -t "$disk_format" -o defaults,rw,user,sync,auto,exec,noatime,nodiratime,nofail "$dev_part" /media/usb0; then
        echo -e "blk-dev-attach $$: \t\t$dev_part was successfully mounted at /media/usb0" >> /dev/kmsg
    else
        echo -e "blk-dev-attach $$: \t\tFailed to mount $dev_part at /media/usb0" >> /dev/kmsg
        rm -f "$LOCKFILE"
        exit 1
    fi
else
    echo -e "blk-dev-attach $$: \tDevice $dev_part already mounted" >> /dev/kmsg
fi

restart_history_container
restart_device_monitor_container

rm -f "$LOCKFILE"

echo "blk-dev-attach $$: Success"  >> /dev/kmsg

exit 0
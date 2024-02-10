#!/bin/bash

# Restarts the history container if it's currently running
restart_history_container() {
    echo -e "Checking if docker is running"
    # Check if Docker is running
    CHECK_IF_DOCKER_IS_UP="$(systemctl --type=service | grep docker.service | awk '{print $3,$4}')"

    if [ "$CHECK_IF_DOCKER_IS_UP" == "active running" ]; then
        echo -e "\tDocker is running. Checking if history container is running"
        history_is_running="$(docker ps -f name=history -q)"
        if [ ! -z "$history_is_running" ]; then
            echo -e "\t\tRestarting history container."
            docker restart $history_is_running 
            return $?
        else 
            echo -e "\t\tHistory container is not running."
        fi
    else
        echo -e "\tDocker is not running yet."
    fi
    return 0
}

# Restarts the device-monitor container if it's currently running
restart_device_monitor_container() {
    echo -e "Checking if docker is running"
    # Check if Docker is running
    CHECK_IF_DOCKER_IS_UP="$(systemctl --type=service | grep docker.service | awk '{print $3,$4}')"

    if [ "$CHECK_IF_DOCKER_IS_UP" == "active running" ]; then
        echo -e "\tDocker is running. Checking if device-monitor container is running"
        device_monitor_is_running="$(docker ps -f name=device-monitor -q)"
        if [ ! -z "$device_monitor_is_running" ]; then
            echo -e "\t\tRestarting device-monitor container."
            docker restart device-monitor
        else 
            echo -e "\t\Device-monitor container is not running."
        fi
    else
        echo -e "\tDocker is not running yet."
    fi
}

rescan_all_scsi_hosts() {
  for host_dir in /sys/class/scsi_host/host*/; do
    host_number=$(basename $host_dir)
    echo "- - -" > /sys/class/scsi_host/$host_number/scan
  done
}

disks_scan(){
    disks=$(lsblk -no NAME | grep "^sd[a-z]$")
    if [ -z "$disks" ]; then
        return 1
    else
        echo "$disks"
        return 0
    fi
}

check_internal_disk_usage(){
    echo "Check internal disk usage:"  
    internal_disk_usage=$(df -h / | tail -1 | awk '{print $5}' | tr -d '%')
    if [ "$internal_disk_usage" -ge 95 ]; then
        echo -e "\tHigh internal disk usage. History container will be stopped."
        docker stop edge-crane history
        return 1
    else
        if [ -d "/mnt/usb0/uploader_folder" ]; then
            echo -e "\The file moving process is running"
        else
            CHECK_IF_DOCKER_IS_UP="$(systemctl --type=service | grep docker.service | awk '{print $3,$4}')"
            if [ "$CHECK_IF_DOCKER_IS_UP" == "active running" ]; then
                if ! docker ps --filter "name=edge-crane" | grep -q "edge-crane"; then
                echo -e "\tStarting edge-crane container." 
                docker restart edge-crane
                fi
            fi
            echo -e "\tOK" 
        fi
    fi
    return 0
}

rescan_all_scsi_hosts

check_internal_disk_usage
history_stop=$?

some_disk_mounted=$(mount -v | grep /media/usb0)

if [ $? -eq 0 ]; then
    echo "Disk registered as mounted in 'mount' command"

    echo -e "\tUpdating kernel partitions:"
    disk=$(echo $some_disk_mounted | awk '{print $1}' | cut -c 6- | rev | cut -c 2- | rev)
    if ! partprobe > /dev/null 2>&1; then
        echo -e "\t\tFail while update kernel partition table"
        echo -e "\t\t\tRemoving disk: $disk"
        echo 1 > /sys/block/$disk/device/delete
        echo -e "\t\tUmounting..."
        umount "/media/usb0"
        echo -e "\t\tRestarting containers"
        if [ "$history_stop" == 0 ]; then
            restart_history_container > /dev/null 2>&1
        fi
        restart_device_monitor_container > /dev/null 2>&1
        exit 0
    else
        echo -e "\t\tOK"
    fi

    echo -e "\tCheck if disk is mounted as read-write (in mount command):"
    echo $some_disk_mounted | grep -q "(rw"
    if [ $? -eq 0 ]; then
        echo -e "\t\tOK"

        echo -e "\tCheck if disk found in 'mount' exists in lsblk:"
        disk=$(echo "$some_disk_mounted" | grep -o '/dev/sd[a-z][0-9]')
        if lsblk $disk > /dev/null 2>&1; then
            echo -e "\t\tOK"
        else
            echo -e "\t\tErro: Disk not exists. Umounting..."
            umount "/media/usb0"
        fi           
    else
        echo -e "\t\tFAIL"
        disk=$(echo $some_disk_mounted | awk '{print $1}' | cut -c 6- | rev | cut -c 2- | rev)
        echo "\tDisk is read only. Removing the disk"
        echo 1 > /sys/block/$disk/device/delete
        echo -e "\tRestarting containers"
        if [ "$history_stop" == 0 ]; then
            restart_history_container
        fi
        restart_device_monitor_container
    fi
else
    echo "No disks registered as mounted in mount command"
    echo "Checking if a disk is available"
    disks=$(disks_scan)
    if [ $? -eq 0 ]; then
        for disk in $disks; do
            dev_disk="/dev/$disk"
            disk_size=$(($(lsblk -b --output SIZE -n -d $dev_disk) / 1024 / 1024 / 1024))
            if [ $disk_size -gt 900 ]; then
                echo -e "\tTrying to mount disk $dev_disk"
                /opt/gabriel/bin/block-device-attach.sh $disk
            fi
        done
    else
        echo -e "\tNo disk found"
    fi
fi
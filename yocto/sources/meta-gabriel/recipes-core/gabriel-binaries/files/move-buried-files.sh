#!/bin/bash

move_buried_files() {
 
  if mountpoint -q /media/usb0; then
    # Verifica e move os arquivos em uploader_folder
    if mountpoint -q /mnt/; then
      echo "already mounted"
    else
      sudo mount --bind -o rw /media/ /mnt/  
    fi

    #logica de verificação da pasta soterrada vazia
    count_files="$(ls -A /mnt/usb0/uploader_folder/ | grep -E '\.ts$|\.mp4$' | wc -l)"
    if [ $count_files -gt 1 ]; then
      sudo systemctl stop block-device-checker > /dev/null 2>&1 &
      docker stop history edge-crane > /dev/null 2>&1 &
      find /mnt/usb0/uploader_folder/ -size 0 -delete;
      sudo ls /mnt/usb0/uploader_folder/ | grep -E '\.ts$|\.mp4$' | xargs -i sudo mv /mnt/usb0/uploader_folder/{} /media/usb0/uploader_folder/tmp/ ;
    else
      echo "Empty"; 
    fi
    count_files_2="$(ls -A /mnt/uploader_folder/tmp/ | grep -E '\.ts$|\.mp4$' | wc -l)"
    if [ $count_files_2 -ge 1 ]; then
      sudo systemctl stop block-device-checker > /dev/null 2>&1 &
      docker stop history edge-crane > /dev/null 2>&1 &
      find /mnt/usb0/uploader_folder/tmp/ -size 0 -delete;
      sudo ls /mnt/usb0/uploader_folder/tmp/ | grep -E '\.ts$|\.mp4$' | xargs -i sudo mv /mnt/usb0/uploader_folder/tmp/{} /media/usb0/uploader_folder/tmp/ ; 
    else
      echo "Empty"; 
    fi
    sudo umount /mnt/ ;
    if [ $(($count_files + $count_files_2)) -ge 2 ]; then
      docker restart history edge-crane device-monitor ; 
      sudo systemctl restart block-device-checker;
      log_file="/home/gabriel/.apps/patcher/log/high_disk_usage.log"
      max_lines=1000
      if [ -e "$log_file" ]; then
          num_lines=$(wc -l "$log_file" | awk '{print $1}')
          if [ "$num_lines" -ge "$max_lines" ]; then
              rm "$log_file"
          fi
      fi
      current_date=$(date '+%Y-%m-%d_%H-%M-%S')
      echo "$current_date - Disk usage high and move files to dir default, $(($count_files + $count_files_2)), files" >> /home/gabriel/.apps/patcher/log/high_disk_usage.log
    else
      echo "not files burrowed"
    fi
  else
    echo "External disk not mounted"    
  fi
  }

move_buried_files
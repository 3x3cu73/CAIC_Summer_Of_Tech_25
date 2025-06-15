#!/bin/bash
set -e

dd if=/dev/urandom of=disk_image.dd bs=1M count=1

# Create ext4 filesystem
mkfs.ext4 disk_image.dd

# Create mount point
MOUNT_POINT=$(mktemp -d)

# Mount the disk image
sudo mount disk_image.dd "$MOUNT_POINT"

# Create some decoy files
echo "System log entries from 2023-05-01" | sudo tee "$MOUNT_POINT/system.log" > /dev/null
echo "Nothing to see here" | sudo tee "$MOUNT_POINT/README.txt" > /dev/null
sudo mkdir -p "$MOUNT_POINT/documents"
echo "Meeting notes for Q2" | sudo tee "$MOUNT_POINT/documents/meeting.txt" > /dev/null

# Create the flag image
convert -size 400x200 xc:black -fill white -pointsize 24 -gravity center \
        -font Adwaita-Mono -draw "text 0,0 'dcCTF{FILE_RECOVERY_SUCCESS}'" flag.png

# Create more decoy files
sudo mkdir -p "$MOUNT_POINT/pictures"
for i in {1..5}; do
    convert -size 100x100 xc:blue -pointsize 14 -gravity center \
            -draw "text 0,0 'Decoy $i'" "$MOUNT_POINT/pictures/image$i.png"
done

# Copy flag to mounted image and delete original
sudo cp flag.png "$MOUNT_POINT/secret_flag.png"
sudo umount "$MOUNT_POINT"

sudo mount disk_image.dd "$MOUNT_POINT"

# Delete the flag file (but it's still recoverable!)
sudo rm "$MOUNT_POINT/secret_flag.png"

sudo umount "$MOUNT_POINT"
rmdir "$MOUNT_POINT"

echo "Created disk image: disk_image.dd (1MB)"

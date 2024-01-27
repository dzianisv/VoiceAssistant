#!/usr/bin/env python3

import sys
import struct
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

# Constants for MBR parsing
SECTOR_SIZE = 512
PARTITION_TABLE_OFFSET = 446
PARTITION_ENTRY_SIZE = 16
PARTITION_TABLE_ENTRIES = 4

def read_mbr(device):
    with open(device, 'rb') as f:
        f.seek(PARTITION_TABLE_OFFSET)
        partition_table = f.read(PARTITION_ENTRY_SIZE * PARTITION_TABLE_ENTRIES)
        return partition_table

def find_last_partition_end(partition_table):
    end_sector = 0
    for i in range(PARTITION_TABLE_ENTRIES):
        offset = i * PARTITION_ENTRY_SIZE
        entry = partition_table[offset:offset + PARTITION_ENTRY_SIZE]
        # Unpack the entry; note that 'I' reads as unsigned int (4 bytes)
        boot_flag, start_chs, part_type, end_chs, start_sector, number_of_sectors = struct.unpack('<B3sB3sII', entry)
        if start_sector and number_of_sectors:
            end_sector = max(end_sector, start_sector + number_of_sectors - 1)
    return end_sector

def calculate_image_size(end_sector):
    return end_sector * SECTOR_SIZE

def copy_device_to_image(input_device, dest_file, size, chunk=1024*1024):
    total = size
    with open(input_device, 'rb') as src:
        while size > 0:
            if size < chunk:
                chunk = size
            size -= chunk
            dest_file.write(src.read(chunk))

def main():
    if len(sys.argv) != 2:
        logger.error(f"Usage: {sys.argv[0]} <block_device>")
        sys.exit(1)

    block_device = sys.argv[1]

    try:
        partition_table = read_mbr(block_device)
        last_partition_end = find_last_partition_end(partition_table)
        image_size = calculate_image_size(last_partition_end+1)
        logger.info("Image size %f/GB", image_size/1024/1024/1024)
        copy_device_to_image(block_device, sys.stdout.buffer, image_size)
        logger.info(f"Backup completed successfully")
    except PermissionError:
        logger.error("Permission denied: this script requires administrative privileges to run.")

if __name__ == "__main__":
    main()
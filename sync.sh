#!/bin/bash

# Recreate directory structure
for dir in control robot_olympics test; do
    python3 -m mpremote fs mkdir :$dir 2>/dev/null
done

# Copy files in root
for file in *.py; do
    [ -f "$file" ] && python3 -m mpremote fs cp "$file" :"$file"
done

# Copy files in subdirectories
for file in control/*.py; do
    [ -f "$file" ] && python3 -m mpremote fs cp "$file" :"$file"
done

for file in robot_olympics/*.py; do
    [ -f "$file" ] && python3 -m mpremote fs cp "$file" :"$file"
done

for file in test/*.py; do
    [ -f "$file" ] && python3 -m mpremote fs cp "$file" :"$file"
done

# Soft reset to clear cached modules
echo "Performing soft reset to clear module cache..."
python3 -m mpremote soft-reset
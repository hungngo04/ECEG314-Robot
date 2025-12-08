#!/bin/bash

echo "Clearing all files from robot..."

# Remove all directories and their contents
for dir in control robot_olympics test; do
    echo "Removing $dir/..."
    python3 -m mpremote fs rm -r :$dir 2>/dev/null || true
done

# Remove root Python files
echo "Removing root .py files..."
python3 -m mpremote exec "import os; [os.remove(f) for f in os.listdir('/') if f.endswith('.py')]" 2>/dev/null || true

echo "Performing soft reset..."
python3 -m mpremote soft-reset

echo "Robot cleared!"

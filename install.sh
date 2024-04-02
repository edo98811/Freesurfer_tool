#!/bin/bash

# Define the line to be added
dir=$(pwd)
line_to_add="source $dir/interface.sh"

# Check if the line already exists in .bashrc
if grep -qxF "$line_to_add" "$HOME/.bashrc"; then
    echo "Already added"
else
    # Add the line to .bashrc
    echo "$line_to_add" >> "$HOME/.bashrc"
    echo "Added the line '$line_to_add' to .bashrc."
fi
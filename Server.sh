#!/bin/bash

# Check if python3 is installed
if ! command -v python3 >/dev/null 2>&1; then
  echo "Please install python3 to run this script."
  exit 1
fi

# Check if index.html file exists
html_file="index.html"
if [ ! -f "$html_file" ]; then
  echo "index.html file not found."
  exit 1
fi

# Start the Python HTTP server
python3 -m http.server 8000 --bind 127.0.0.1 --directory "$(dirname "$html_file")"


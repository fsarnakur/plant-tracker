#!/data/data/com.termux/files/usr/bin/bash

# Path to your project
cd ~/plant-tracker

# Step 1: Export HTML from database
python export.py

# Step 2: Start server (in background)
nohup python -m http.server 8080 > /dev/null 2>&1 &

# Step 3: Wait a second for the server to start
sleep 1

# Step 4: Open Chrome to the local address
termux-open-url http://localhost:8080/plants.html

#!/usr/bin/env bash
set -e
echo "Training the Rasa model..."
rasa train
echo "Starting action server in background..."
rasa run actions &
echo "Starting Rasa server (open another terminal for rasa shell if needed)..."
rasa run --enable-api

#!/usr/bin/env bash
#5.5.0/run.sh

docker build -t "vicon_position" .
port="$1"

python ViconPosition.py "$port" &

xhost +
sudo docker run --env="semantix_port=$port" --network="host" "vicon_position"

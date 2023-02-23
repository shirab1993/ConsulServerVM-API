#!/bin/bash

# Build and Run docker container
docker build -t api .
docker run -d -p 8080:5000 -v /var/run/docker.sock:/var/run/docker.sock api

echo "#######################################################"
echo " docker container running - go to my app: http://192.168.50.10:8080/v1/api/consulCluster/status "
echo "#######################################################"


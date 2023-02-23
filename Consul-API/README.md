# Consul-API 
**Read the following instructions.**

### Requirements

1. Install virtualbox version:6.1
2. Install vagrant(version:2.2.9)on your terminal.


### Step one
1. Clone this repository.
2. change directory to: 
~~~
cd ConsulServerVM-API/Consul-API
~~~
3. Execute the script: vagrant_up.sh
~~~
chmod +x vagrant_up.sh
~~~

~~~
./vagrant_up.sh
~~~
The script excute the commands:
`vagrant up`  will spawn a VM according to the configuration written in the Vagrantfile, it will install and run consul-server and install docker on the machine.
`vagrant ssh` give you access to the shell of the running Vagrant machine.
 
 
### Step two
1.change directory to: 
~~~
cd /vagrant
~~~
2. Run docker commands:
~~~
docker build -t api .
~~~

~~~
docker run -d -p 8080:5000 -v /var/run/docker.sock:/var/run/docker.sock api
~~~
The script excute the commands:
`docker build -t api .` use Dockerfile to build a docker image called api, and run python api service .
`docker run -d -p 8080:5000 -v /var/run/docker.sock:/var/run/docker.sock api` 
run a container in background, binding the port 8080 ->5000 and create volume for Communicate with the Docker daemon from within a container.



### API Service

1. The API service expose the following routes:
you should see the resonse http://192.168.50.10:8080
~~~
GET  /v1/api/consulCluster/status
GET  /v1/api/consulCluster/summary
GET  /v1/api/consulCluster/members
GET  /v1/api/consulCluster/systemInfo
~~~

#### status
This endpoint will sample the Consul server API to see if it is available or not, and will return the result in the following format:
`{"status": 0|1, "message": "<message>"}`

Where:
* Status 0 means down and 1 means up
* Message should indicate when the sampling was successfull or give a relevant error message in case it is down

##### Response example

~~~
{"status": "1", "message": "Consul server is running"}
~~~

#### summary
This endpoint will sample the Consul API to get the following information about the cluser:
 - Number of registered nodes
 - Number of registered services
 - Cluster Leader IP and port
 - The internal protocol version used by Consul

##### Response example
~~~
{
"cluster_protocol":"1.10.3",
"leader":"192.168.50.10",
"num_nodes":1,
"num_services":1
}
~~~


#### members
This endpoint will sample the Consul API to get the list of registered nodes in the culster in the following format:

##### Response example
~~~
{
"registered_nodes":[
"consul-server"
 ]
}
~~~


#### systemInfo
This endpoint will expose metrics taken from the docker container. 

~~~
{
"MemoryGB":1,
"container_resource_limits":{"cpu_limit":0,"memory_limit":0},
"container_restart_count":0,
"container_version":"api",
"cpu_percent":0.1,
"disk_usage":4435161088,
"memory_usage":179302400,
"network_bytes_recv":29911,
"network_bytes_sent":14322,
"vCpus":1
}
~~~


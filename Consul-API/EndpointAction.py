from flask import Flask, jsonify
import requests
import psutil
import docker


class EndpointAction:
    def __init__(self, url):
        self.url = url

    def handle_status(self):
        try:
            # Send a GET request to Consul server API to check its status
            response = requests.get(self.url + '/v1/status/leader')

            # If the response is successful, return a JSON response with status 0 and success message
            if response.status_code == 200:
                return jsonify({'status': 1, 'message': 'Consul server is running.'})

            # If the response is not successful, return a JSON response with status 1 and error message
            else:
                return jsonify({'status': 0, 'message': 'Consul server unavailable.'})

        # If there is an exception, return a JSON response with status 1 and error message
        except Exception as e:
            return error_handler('status', str(e))

    def handle_summary(self):
        try:
            # Send a GET request to Consul server API to get the summary information
            response = requests.get(self.url + '/v1/status/leader')
            leader_ip_port = response.text[1:].split(':')[0]

            response = requests.get(f'http://{leader_ip_port}:8500/v1/catalog/nodes')
            num_nodes = len(response.json())

            response = requests.get(f'http://{leader_ip_port}:8500/v1/catalog/services')
            num_services = len(response.json())

            response = requests.get(f'http://{leader_ip_port}:8500/v1/agent/self')
            protocol_version = response.json()['Config']['Version']

            # Return a JSON response with the summary information
            return jsonify({'num_nodes': num_nodes, 'num_services': num_services, 'leader': leader_ip_port,
                            'cluster_protocol': protocol_version})

        # If there is an exception, return a JSON response with status 1 and error message
        except Exception as e:
            return error_handler('summary', str(e))

    def handle_member(self):
        response = requests.get(self.url + '/v1/agent/members')

        if response.status_code == 200:
            members = [member['Name'] for member in response.json()]
            return jsonify({'registered_nodes': members})
        else:
            return jsonify({'message': 'Failed to retrieve registered nodes from Consul API', 'status': 1})


def error_handler(error_type, error_message):
    return jsonify(
        {'status': 0, 'message': 'An error occurred while getting the ' + error_type + 'information. The error is: ' +
                                 error_message})


def handle_system_info():
    # Get Docker container info
    client = docker.from_env()

    for container in client.containers.list():
        container_id = container.id

    container = client.containers.get(container_id)

    # Get system metrics
    vcpus = psutil.cpu_count()
    mem_gb = round(psutil.virtual_memory().total / (1024.0 ** 3))
    cpu_percent = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().used
    network_bytes_sent = psutil.net_io_counters().bytes_sent
    network_bytes_recv = psutil.net_io_counters().bytes_recv
    disk_usage = psutil.disk_usage('/').used
    container_restart_count = container.attrs['RestartCount']
    container_resource_limits = {
        'cpu_limit': container.attrs['HostConfig']['CpuQuota'],
        'memory_limit': container.attrs['HostConfig']['Memory']
    }
    container_version = container.attrs['Config']['Image']

    # Build response
    response = {
        'vCpus': vcpus,
        'MemoryGB': mem_gb,
        'cpu_percent': cpu_percent,
        'memory_usage': memory_usage,
        'network_bytes_sent': network_bytes_sent,
        'network_bytes_recv': network_bytes_recv,
        'disk_usage': disk_usage,
        'container_restart_count': container_restart_count,
        'container_resource_limits': container_resource_limits,
        'container_version': container_version
    }

    return jsonify(response)

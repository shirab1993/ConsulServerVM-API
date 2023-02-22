from flask import Flask, jsonify
from EndpointAction import EndpointAction as RoutesHandler
import EndpointAction

app = Flask(__name__)
url = 'http://192.168.50.10:8500'


@app.route('/v1/api/consulCluster/status')
def consul_cluster_status():
    return RoutesHandler(url).handle_status()


@app.route('/v1/api/consulCluster/summary')
def consul_cluster_summary():
    return RoutesHandler(url).handle_summary()

@app.route('/v1/api/consulCluster/members')
def get_registered_nodes():
    return RoutesHandler(url).handle_member()


@app.route('/v1/api/consulCluster/systemInfo', methods=['GET'])
def system_info():
    return EndpointAction.handle_system_info()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


    

    

from cloudify.exceptions import NonRecoverableError
from cloudify.decorators import operation
from cloudify import ctx
import os
import subprocess
import time
from cloudify.state import ctx_parameters as inputs


def start_master(master_port):
    subprocess.call(
    	'sudo docker run --net=host -d -v '
    	'/var/run/docker.sock:/var/run/docker.sock '
    	'gcr.io/google_containers/hyperkube:v1.0.1 '
    	'/hyperkube kubelet '
    	'--api-servers=http://localhost:{0} --v=2 '
    	'--address=0.0.0.0 --enable-server '
    	'--hostname-override=127.0.0.1 '
    	'--config=/etc/kubernetes/manifests-multi '
    	'--cluster-dns=10.0.0.10 '
    	'--cluster-domain=cluster.local'.format(master_port),
    	shell=True
    )


if __name__ == '__main__':
    os.chdir(os.path.expanduser("~"))
    os.system('sudo service docker start')
    master_port = inputs['master_port']
    start_master(master_port)

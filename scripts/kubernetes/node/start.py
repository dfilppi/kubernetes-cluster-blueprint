from cloudify.decorators import operation
from cloudify.exceptions import NonRecoverableError
from cloudify import ctx
import os
import subprocess
import time
import socket
import fcntl
import struct
from cloudify.state import ctx_parameters as inputs


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(
        fcntl.ioctl(s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15]))[20:24])


def remove_docker_bridge():

    os.system('sudo /sbin/ifconfig docker0 down')
    os.system('sudo apt-get install -y bridge-utils')
    os.system('sudo brctl delbr docker0')


def start_node(master_ip, master_port):
    subprocess.call(
        'sudo docker run --net=host -d -v '
        '/var/run/docker.sock:/var/run/docker.sock '
        'gcr.io/google_containers/hyperkube:v1.0.1 '
        '/hyperkube kubelet --api-servers=http://{0}:{1} '
        '--v=2 --address=0.0.0.0 --enable-server '
        '--hostname-override={2} --cluster-dns=10.0.0.10 '
        '--cluster-domain=cluster.local'.format(
            master_ip, master_port, get_ip_address('eth0')
        ),
        shell=True
    )


if __name__ == '__main__':

    ctx.logger.info('Starting Kubernetes Node')

    master_ip = inputs['master_ip']
    ctx.logger.info('Master IP: {0}'.format(master_ip))

    master_port = inputs['master_port']
    ctx.logger.info('Master Port: {0}'.format(master_port))

    remove_docker_bridge()

    os.system('sudo service docker start')

    start_node(master_ip, master_port)

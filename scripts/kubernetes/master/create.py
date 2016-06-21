from cloudify.exceptions import NonRecoverableError
from cloudify.decorators import operation
from cloudify import ctx
import os
import subprocess
import time
from cloudify.state import ctx_parameters as inputs


def remove_docker_bridge():

    os.system('sudo /sbin/ifconfig docker0 down')
    os.system('sudo apt-get install -y bridge-utils')
    os.system('sudo brctl delbr docker0')


if __name__ == '__main__':

    remove_docker_bridge()

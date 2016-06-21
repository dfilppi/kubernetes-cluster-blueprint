from cloudify.exceptions import NonRecoverableError
from cloudify.decorators import operation
from cloudify import ctx
import os
import subprocess
import time
from cloudify.state import ctx_parameters as inputs


def run_flannel():

    pipe = subprocess.Popen(
        ['sudo', 'docker','-H', 'unix:///var/run/docker-bootstrap.sock',
        'run', '-d', '--net=host', '--privileged', '-v',
        '/dev/net:/dev/net', 'quay.io/coreos/flannel:0.5.3'],
        stderr=open('/dev/null'),
        stdout=subprocess.PIPE
    )

    container_id = pipe.stdout.read().strip()

    pipe.wait()

    output = os.popen(
        'sudo docker -H unix:///var/run/docker-bootstrap.sock '
        'exec {0} cat /run/flannel/subnet.env'.format(
            container_id
        )
    )

    flannel = ';'.join(output.read().split())

    return flannel


if __name__ == '__main__':

    ctx.logger.info('Initializing Flannel')

    os.system("sudo service docker stop")

    flannel = run_flannel()

    ctx.instance.runtime_properties['flannel'] = flannel

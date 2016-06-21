import subprocess
import time
import os
from cloudify import ctx

def docker_bootstrap():
    output = subprocess.Popen(
        ['sudo', 'nohup', 'docker', 'daemon',
        '-H', 'unix:///var/run/docker-bootstrap.sock',
        '-p', '/var/run/docker-bootstrap.pid',
        '--iptables=false', '--ip-masq=false',
        '--bridge=none', '--graph=/var/lib/docker-bootstrap'],
        stdout=open('/dev/null'),
        stderr=open('/tmp/docker-bootstrap.log','w'),
        stdin=open('/dev/null')
    )

    ctx.logger.info('Output: {0}'.format(output.pid))


if __name__ == '__main__':

    ctx.logger.info('Initializing Docker Bootstrap')
    docker_bootstrap()
    time.sleep(15)

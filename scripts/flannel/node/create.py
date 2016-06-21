from cloudify.exceptions import NonRecoverableError
from cloudify import ctx
import os
import subprocess
import time
from cloudify.state import ctx_parameters as inputs

CMD_APP = 'DOCKER_OPTS="--bip=${FLANNEL_SUBNET} --mtu=${FLANNEL_MTU}"'


def run_flannel(ip, flannel_version):

    pipe = subprocess.Popen(
        ['sudo', 'docker', '-H',
         'unix:///var/run/docker-bootstrap.sock',
         'run', '-d', '--net=host', '--privileged',
         '-v', '/dev/net:/dev/net',
         'quay.io/coreos/flannel:{0}'.format(flannel_version),
         '/opt/bin/flanneld',
         '--etcd-endpoints=http://{0}:4001'.format(ip)],
        stderr=open('/dev/null'),
        stdout=subprocess.PIPE
    )

    container_id = pipe.stdout.read().strip()

    pipe.wait()
    
    output = os.popen(
        'sudo docker -H unix:///var/run/docker-bootstrap.sock '
        'exec {0} cat /run/flannel/subnet.env'.format(
          container_id)
    )

    flannel = ";".join(output.read().split())

    return flannel


def edit_docker_config(flannel):

    with open('/tmp/docker', 'w') as fd:
        with open('/etc/default/docker', 'r') as fdin:
            for line in fdin:
                fd.write(line)

    with open('/tmp/docker', 'a') as fd:
        fd.write('{0}\n'
                 '{1}\n'.format(flannel, CMD_APP)
                 )

    try:
        subprocess.call('sudo mv /tmp/docker /etc/default/docker', shell=True)
    except:
        raise NonRecoverableError('Unable to move Docker config into place.')


if __name__ == '__main__':

    time.sleep(10)

    ctx.logger.info('Initializing Flannel')

    os.system("sudo service docker stop")

    master_ip = inputs['master_ip']

    version = inputs['flannel_version']

    ctx.logger.info('Master IP: {0}'.format(master_ip))

    ctx.instance.runtime_properties['flannel'] = run_flannel(master_ip, version)

    flannel_args = ctx.instance.runtime_properties['flannel']

    ctx.logger.info('Flannel: {0}'.format(flannel_args))

    edit_docker_config(flannel_args)
